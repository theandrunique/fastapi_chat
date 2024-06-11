from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    username: str
    email: str
    email_verified: bool
    image_url: str | None = None
    active: bool
    created_at: datetime
