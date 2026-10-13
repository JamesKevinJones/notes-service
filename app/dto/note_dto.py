from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoteCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = ""


class NoteUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = None


class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
