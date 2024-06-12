from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel
from src.models.chat import ChatType
from src.models.message import Message


class ChatCreate(BaseModel):
    name: str | None


@dataclass(kw_only=True)
class ChatFactory:
    name: str | None = None
    creator_id: UUID | None = None
    type: ChatType
    members: list[UUID]
    image_url: str | None = None
    admins: list[UUID] = field(default_factory=lambda: list())
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    message_count: int = 0
    last_message: Message | None = None

    def model_dump(self) -> dict[str, Any]:
        return asdict(self)
