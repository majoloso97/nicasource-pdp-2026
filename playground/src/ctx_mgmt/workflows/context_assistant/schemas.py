from typing import Optional

from drf_pydantic import BaseModel as DRFBaseModel
from pydantic import Field

from .constants import DEFAULT_SIMILARITY_THRESHOLD, DEFAULT_TOP_K


class ChatRequest(DRFBaseModel):
    client_slug: str = Field(..., description="Client scope for context isolation")
    message: str
    conversation_id: Optional[str] = None
    top_k: int = DEFAULT_TOP_K
    similarity_threshold: float = DEFAULT_SIMILARITY_THRESHOLD
