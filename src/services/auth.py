from dataclasses import dataclass

from src.models.user import User
from src.services.base.base_auth import AuthService
from src.services.base.base_jwt import JWTService
from src.services.base.base_users import UsersService


@dataclass(kw_only=True)
class ImplAuthService(AuthService):
    users_service: UsersService
    jwt_service: JWTService

    async def authenticate(self, token: str) -> User | None:
        token_payload = self.jwt_service.decode(token)
        if token_payload is None:
            return None
        user = await self.users_service.get(token_payload.sub)
        if user is None:
            return None
        return user
