from abc import ABC
from dataclasses import dataclass

from src.models.user import User
from .base_jwt import JWTService


@dataclass(kw_only=True)
class AuthService(ABC):
    jwt_service: JWTService

    async def authenticate(self, token: str) -> User | None: ...
