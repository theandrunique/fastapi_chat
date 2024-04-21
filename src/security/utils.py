from pydantic import ValidationError
import jwt

from .exceptions import InvalidToken
from .config import settings
from .schemas import TokenPayload

def decode_payload(
    token: str,
) -> TokenPayload:
    try:
        payload_dict = jwt.decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return TokenPayload(**payload_dict)
    except (jwt.PyJWTError, ValidationError):
        raise InvalidToken()
