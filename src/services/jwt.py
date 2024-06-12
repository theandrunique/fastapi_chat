from dataclasses import dataclass

import jwt
from pydantic import ValidationError

from src.schemas.token_payload import TokenPayload
from .base.base_jwt import JWTService


@dataclass(kw_only=True)
class PyJWTService(JWTService):
    auth_server_url: str
    client_id: str
    algorithm: str

    def _get_signing_key(self, token: str):
        url = f"{self.auth_server_url}/.well-known/jwks.json"
        jwks_client = jwt.PyJWKClient(url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        return signing_key.key

    def decode(self, token: str) -> TokenPayload | None:
        try:
            signing_key = self._get_signing_key(token)
            payload_dict = jwt.decode(
                jwt=token,
                key=signing_key,
                algorithms=[self.algorithm],
                audience=self.client_id,
                issuer=self.auth_server_url,
            )
            return TokenPayload(**payload_dict)
        except (jwt.PyJWTError, ValidationError):
            return None
