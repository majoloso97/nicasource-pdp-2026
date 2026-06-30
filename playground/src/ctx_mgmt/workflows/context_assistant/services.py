import math
from dataclasses import dataclass

from ctx_mgmt.models import Document, DocumentChunk
from django.conf import settings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from .constants import TRIVIAL_DIRECT_MESSAGES
from .prompts import build_router_prompt
from .state import RouteDecision


def estimate_tokens(text: str) -> int:
    return max(1, math.ceil(len(text) / 4)) if text else 0


def embed_text(text: str) -> list[float]:
    emb = OpenAIEmbeddings(model=settings.EMBEDDINGS_MODEL)
    v = emb.embed_query(text)
    return [float(x) for x in v]


def chunk_text(text: str, *, chunk_chars: int = 900, overlap: int = 120) -> list[str]:
    text = (text or "").strip()
    if not text:
        return []

    chunks: list[str] = []
    i = 0
    while i < len(text):
        end = min(len(text), i + chunk_chars)
        chunk = text[i:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        i = max(0, end - overlap)
    return chunks


def ensure_document_chunks(document: Document) -> int:
    if document.chunks.exists():
        return document.chunks.count()

    chunks = chunk_text(document.content)
    objs: list[DocumentChunk] = []
    for idx, content in enumerate(chunks):
        v = embed_text(content)
        objs.append(
            DocumentChunk(
                document=document,
                idx=idx,
                content=content,
                token_estimate=estimate_tokens(content),
                embedding=v,
            )
        )
    DocumentChunk.objects.bulk_create(objs)
    return len(objs)


def get_llm():
    return ChatOpenAI(model=settings.CHAT_MODEL)


@dataclass(frozen=True)
class RetrievedChunk:
    document_title: str
    chunk_id: int
    content: str
    token_estimate: int


def route_with_llm(message: str) -> tuple[bool, str, str]:
    llm = get_llm()
    try:
        router = llm.with_structured_output(RouteDecision)
        decision = router.invoke(build_router_prompt(message))
        return decision.needs_retrieval, decision.reason, "llm"
    except Exception:
        return route_with_fallback(message)


def route_with_fallback(message: str) -> tuple[bool, str, str]:
    normalized = (message or "").strip().lower()
    if normalized in TRIVIAL_DIRECT_MESSAGES:
        return False, "Trivial conversational message; retrieval skipped.", "fallback"

    if len(normalized.split()) <= 2 and "?" not in normalized:
        return (
            False,
            "Very short conversational message; retrieval skipped.",
            "fallback",
        )

    return (
        True,
        "Defaulted to retrieval for a non-trivial client/project question.",
        "fallback",
    )
