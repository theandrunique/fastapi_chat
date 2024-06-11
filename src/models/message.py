from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, AliasChoices


class Message(BaseModel):
    id: int = Field(validation_alias=AliasChoices("_id", "id"))
    text: str
    timestamp: datetime
    from_id: UUID
    attachments: list[str] | None
