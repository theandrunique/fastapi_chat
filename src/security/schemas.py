import datetime
from uuid import UUID

from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: int
    jti: UUID
    exp: datetime.datetime
