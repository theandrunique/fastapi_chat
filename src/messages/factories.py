from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from uuid import UUID


@dataclass
class MessageFactory:
    id: int
    text: str
    from_id: UUID
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    attachments: list[str] | None = None

    def model_dump(self):
        d = asdict(self)
        d["_id"] = d.pop("id")
        return d
