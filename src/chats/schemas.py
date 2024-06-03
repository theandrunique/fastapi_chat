from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID
from enum import Enum

from src.mongo import PyObjectId
from src.messages.schemas import Message

from pydantic import BaseModel, Field, AliasChoices


class ChatType(str, Enum):
    PRIVATE = "private"
    GROUP = "group"


class Chat(BaseModel):
    id: PyObjectId = Field(validation_alias=AliasChoices("_id", "id"))
    name: str | None = None
    created_at: datetime
    creator_id: UUID | None = None
    members: list[UUID]
    admins: list[UUID]
    message_count: int
    last_message: Message | None = None
    type: ChatType


class ChatCreate(BaseModel):
    name: str | None


@dataclass(kw_only=True)
class ChatFactory:
    name: str | None = None
    creator_id: UUID | None = None
    type: ChatType
    members: list[UUID]
    admins: list[UUID] = field(default_factory=lambda: list())
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    message_count: int = 0
    last_message: Message | None = None

    def model_dump(self) -> dict[str, Any]:
        return asdict(self)
