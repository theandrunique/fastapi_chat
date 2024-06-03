from pydantic import ValidationError
import jwt
from jwt import PyJWKClient

from src.logger import logger

from .config import settings
from .schemas import TokenPayload


def get_signing_key(token: str):
    url = f"{settings.AUTHORIZATION_SERVER_URL}/.well-known/jwks.json"
    jwks_client = PyJWKClient(url)
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    return signing_key.key


def decode_payload(
    token: str,
) -> TokenPayload | None:
    try:
        signing_key = get_signing_key(token)
        payload_dict = jwt.decode(
            jwt=token,
            key=signing_key,
            algorithms=[settings.ALGORITHM],
            audience=settings.CLIENT_ID,
            issuer="http://localhost:8000",
        )
        return TokenPayload(**payload_dict)
    except (jwt.PyJWTError, ValidationError) as e:
        logger.error(f"Invalid token: {e}")
        return None
