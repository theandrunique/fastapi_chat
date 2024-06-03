from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.security.exceptions import InvalidToken
from src.security.schemas import TokenPayload
from src.security.utils import decode_payload


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    auto_error=False,
)


def user_authentication(
    token: str = Depends(oauth2_scheme),
) -> TokenPayload:
    payload = decode_payload(token)
    if not payload:
        raise InvalidToken()
    return payload


UserAuthorization = Annotated[TokenPayload, Depends(user_authentication)]
