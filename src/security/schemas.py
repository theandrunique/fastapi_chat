from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: UUID
    exp: datetime
    scopes: list[str]
    aud: str
    exp: datetime
    iss: str
    
