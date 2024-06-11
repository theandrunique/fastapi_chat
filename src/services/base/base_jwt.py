from abc import ABC, abstractmethod

from src.schemas.token_payload import TokenPayload


class JWTService(ABC):
    @abstractmethod
    def decode(self, token: str) -> TokenPayload | None: ...
