from langgraph.graph import END, START, StateGraph

from .nodes import (
    build_context_packet,
    generate_response,
    load_client_and_conversation,
    load_recent_messages,
    retrieve_documents,
    route_question,
    route_to_next,
    summarize_history,
    update_memory,
)
from .state import GraphState


builder = StateGraph(GraphState)
builder.add_node("load", load_client_and_conversation)
builder.add_node("route_question", route_question)
builder.add_node("retrieve_documents", retrieve_documents)
builder.add_node("summarize_history", summarize_history)
builder.add_node("load_recent", load_recent_messages)
builder.add_node("build_context", build_context_packet)
builder.add_node("generate", generate_response)
builder.add_node("update_memory", update_memory)

builder.add_edge(START, "load")
builder.add_edge("load", "route_question")

builder.add_conditional_edges(
    "route_question",
    route_to_next,
    {
        "retrieve_and_summarize": "retrieve_documents",
        "retrieve": "retrieve_documents",
        "summarize": "summarize_history",
        "direct": "load_recent",
    },
)

builder.add_edge("retrieve_documents", "summarize_history")
builder.add_edge("summarize_history", "load_recent")
builder.add_edge("load_recent", "build_context")
builder.add_edge("build_context", "generate")
builder.add_edge("generate", "update_memory")
builder.add_edge("update_memory", END)

context_assistant_workflow = builder.compile()
