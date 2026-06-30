from datetime import datetime, timezone
from typing import Any

from ctx_mgmt.models import Client, Conversation, DocumentChunk, Message

from .constants import (
    MAX_CONTEXT_TOKENS,
    RECENT_MESSAGES_TO_KEEP,
    SUMMARIZE_AFTER_MESSAGES,
)
from .prompts import ASSISTANT_SYSTEM_PROMPT, build_summary_prompt
from .services import (
    RetrievedChunk,
    embed_text,
    estimate_tokens,
    get_llm,
    route_with_llm,
)
from .state import GraphState

from pgvector.django import CosineDistance


def load_client_and_conversation(state: GraphState) -> dict[str, Any]:
    client = Client.objects.get(slug=state.client_slug)
    if state.conversation_id:
        conv = Conversation.objects.get(id=state.conversation_id, client=client)
    else:
        conv = Conversation.objects.create(client=client)

    return {"client_id": client.id, "conversation_pk": str(conv.id)}


def route_question(state: GraphState) -> dict[str, Any]:
    msg = (state.message or "").lower()
    wants_docs, route_reason, route_source = route_with_llm(msg)

    conv = Conversation.objects.get(id=state.conversation_pk)
    msg_count = conv.messages.count()
    needs_summary = msg_count >= SUMMARIZE_AFTER_MESSAGES

    if wants_docs and needs_summary:
        route = "retrieve_and_summarize"
    elif wants_docs:
        route = "retrieve"
    elif needs_summary:
        route = "summarize"
    else:
        route = "direct"

    return {
        "route": route,
        "debug_info": {
            **(state.debug_info or {}),
            "route": route,
            "route_reason": route_reason,
            "route_source": route_source,
            "needs_retrieval": wants_docs,
        },
    }


def retrieve_documents(state: GraphState) -> dict[str, Any]:
    client = Client.objects.get(id=state.client_id)
    query_vec = embed_text(state.message)

    max_distance = 1.0 - state.similarity_threshold
    qs = DocumentChunk.objects.filter(document__client=client)
    qs = (
        qs.alias(distance=CosineDistance("embedding", query_vec))
        .filter(distance__lte=max_distance)
        .order_by("distance")
    )

    chunks = list(qs.select_related("document")[: max(1, int(state.top_k))])
    retrieved = [
        RetrievedChunk(
            document_title=c.document.title,
            chunk_id=c.id,
            content=c.content,
            token_estimate=c.token_estimate,
        )
        for c in chunks
    ]
    return {
        "retrieved_chunks": [
            {
                "document_title": r.document_title,
                "chunk_id": r.chunk_id,
                "content": r.content,
                "token_estimate": r.token_estimate,
            }
            for r in retrieved
        ],
        "debug_info": {
            **(state.debug_info or {}),
            "retrieved": [
                {"document_title": r.document_title, "chunk_id": r.chunk_id}
                for r in retrieved
            ],
        },
    }


def summarize_history(state: GraphState) -> dict[str, Any]:
    conv = Conversation.objects.get(id=state.conversation_pk)
    msgs = list(conv.messages.order_by("created_at"))
    if len(msgs) <= SUMMARIZE_AFTER_MESSAGES:
        return {
            "running_summary": conv.running_summary,
            "debug_info": {
                **(state.debug_info or {}),
                "summary_used": bool(conv.running_summary),
            },
        }

    older = msgs[: max(0, len(msgs) - RECENT_MESSAGES_TO_KEEP)]
    older_text = "\n".join(f"{m.role}: {m.content}" for m in older)

    llm = get_llm()
    new_summary = llm.invoke(
        build_summary_prompt(conv.running_summary, older_text)
    ).content

    conv.running_summary = new_summary
    conv.summary_updated_at = datetime.now(tz=timezone.utc)
    conv.save(update_fields=["running_summary", "summary_updated_at", "updated_at"])

    return {
        "running_summary": new_summary,
        "debug_info": {**(state.debug_info or {}), "summary_used": True},
    }


def load_recent_messages(state: GraphState) -> dict[str, Any]:
    conv = Conversation.objects.get(id=state.conversation_pk)
    recent = list(
        conv.messages.order_by("-created_at").values("role", "content")[
            :RECENT_MESSAGES_TO_KEEP
        ]
    )
    recent.reverse()
    return {"recent_messages": recent}


def build_context_packet(state: GraphState) -> dict[str, Any]:
    summary = (state.running_summary or "").strip()
    recent = state.recent_messages or []
    retrieved = state.retrieved_chunks or []

    parts: list[tuple[str, str]] = [("SYSTEM", ASSISTANT_SYSTEM_PROMPT)]
    if summary:
        parts.append(("RUNNING SUMMARY", summary))

    if recent:
        recent_text = "\n".join(f"{m['role']}: {m['content']}" for m in recent)
        parts.append(("RECENT MESSAGES", recent_text))

    if retrieved:
        docs_text = "\n\n".join(
            f"[{c['document_title']}#{c['chunk_id']}]\n{c['content']}"
            for c in retrieved
        )
        parts.append(("RETRIEVED DOCUMENTS", docs_text))

    parts.append(("USER QUESTION", state.message))

    packet = "\n\n".join(f"{title}:\n{body}" for title, body in parts)
    token_est = estimate_tokens(packet)

    if token_est > MAX_CONTEXT_TOKENS and retrieved:
        parts = [p for p in parts if p[0] != "RETRIEVED DOCUMENTS"]
        packet = "\n\n".join(f"{title}:\n{body}" for title, body in parts)
        token_est = estimate_tokens(packet)

    if token_est > MAX_CONTEXT_TOKENS and summary:
        truncated = summary[-1200:]
        parts = [
            (t, b) if t != "RUNNING SUMMARY" else (t, truncated) for (t, b) in parts
        ]
        packet = "\n\n".join(f"{title}:\n{body}" for title, body in parts)
        token_est = estimate_tokens(packet)

    dbg = {
        **(state.debug_info or {}),
        "client": state.client_slug,
        "recent_messages": len(recent),
        "estimated_input_tokens": token_est,
    }
    return {"context_packet": packet, "token_estimate": token_est, "debug_info": dbg}


def generate_response(state: GraphState) -> dict[str, Any]:
    llm = get_llm()
    content = llm.invoke(state.context_packet).content
    return {"response": content}


def update_memory(state: GraphState) -> dict[str, Any]:
    conv = Conversation.objects.get(id=state.conversation_pk)

    user_tokens = estimate_tokens(state.message)
    assistant_tokens = estimate_tokens(state.response)
    Message.objects.create(
        conversation=conv,
        role=Message.Role.USER,
        content=state.message,
        token_estimate=user_tokens,
    )
    Message.objects.create(
        conversation=conv,
        role=Message.Role.ASSISTANT,
        content=state.response,
        token_estimate=assistant_tokens,
    )

    dbg = {
        **(state.debug_info or {}),
        "summary_used": bool(state.running_summary),
        "estimated_output_tokens": assistant_tokens,
        "estimated_total_tokens": int(state.token_estimate or 0) + assistant_tokens,
    }
    return {"debug_info": dbg}


def route_to_next(state: GraphState) -> str:
    return state.route or "direct"
