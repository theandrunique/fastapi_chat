from typing import Annotated

from fastapi import Security
from src.security.dependencies import user_authentication
from src.security.schemas import TokenPayload


UserAuthorization = Annotated[TokenPayload, Security(user_authentication)]
