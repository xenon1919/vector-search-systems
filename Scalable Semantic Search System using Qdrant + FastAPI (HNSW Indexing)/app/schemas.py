from typing import Any

from pydantic import BaseModel, Field


class DocumentIn(BaseModel):
	id: int = Field(..., description="Unique document identifier")
	text: str = Field(..., min_length=1)
	category: str | None = None
	metadata: dict[str, Any] = Field(default_factory=dict)


class IngestRequest(BaseModel):
	documents: list[DocumentIn]


class SearchRequest(BaseModel):
	query: str = Field(..., min_length=1)
	limit: int = Field(default=5, ge=1, le=50)
	category: str | None = None


class SearchHit(BaseModel):
	id: int | str
	text: str
	category: str | None = None
	score: float
	payload: dict[str, Any]


class SearchResponse(BaseModel):
	results: list[SearchHit]
