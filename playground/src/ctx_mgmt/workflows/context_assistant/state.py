from typing import Any, Optional

from pydantic import BaseModel, Field

from .constants import DEFAULT_SIMILARITY_THRESHOLD, DEFAULT_TOP_K


class RouteDecision(BaseModel):
    needs_retrieval: bool
    reason: str


class GraphState(BaseModel):
    client_slug: str
    message: str
    conversation_id: Optional[str] = None
    top_k: int = DEFAULT_TOP_K
    similarity_threshold: float = DEFAULT_SIMILARITY_THRESHOLD

    client_id: Optional[int] = None
    conversation_pk: Optional[str] = None
    route: Optional[str] = None

    running_summary: str = ""
    recent_messages: list[dict[str, Any]] = Field(default_factory=list)
    retrieved_chunks: list[dict[str, Any]] = Field(default_factory=list)
    context_packet: str = ""
    response: str = ""

    token_estimate: int = 0
    debug_info: dict[str, Any] = Field(default_factory=dict)
