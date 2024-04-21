import datetime
from uuid import UUID

from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str
    jti: UUID
    exp: datetime.datetime
