from dataclasses import dataclass
import httpx

from uuid import UUID
from src.models.user import User
from src.services.base.base_users import UsersService


@dataclass(kw_only=True)
class ImplUsersService(UsersService):
    auth_service_url: str

    async def get(self, id: UUID) -> User | None:
        async with httpx.AsyncClient(base_url=self.auth_service_url) as client:
            response = await client.get(f"/users/{id}")
            if response.status_code == 200:
                return User(**response.json())
            return None
