from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from app.infra.security.auth_settings import AuthSettings


class JwtService:
    def __init__(self, auth_settings: AuthSettings) -> None:
        self.auth_settings = auth_settings

    def create_access_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None,
        extra_claims: dict[str, Any] | None = None,
    ) -> str:
        to_encode = data.copy()
        if extra_claims:
            to_encode.update(extra_claims)

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.auth_settings.access_token_expire_minutes
            )
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            self.auth_settings.secret_key,
            algorithm=self.auth_settings.algorithm,
        )
        return encoded_jwt

    def decode_access_token(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                self.auth_settings.secret_key,
                algorithms=[self.auth_settings.algorithm],
            )
        except jwt.ExpiredSignatureError as exc:
            raise ValueError("Access token has expired") from exc
        except jwt.InvalidTokenError as exc:
            raise ValueError("Invalid access token") from exc

        subject = payload.get("sub")
        if not isinstance(subject, str) or not subject.strip():
            raise ValueError("Access token missing required claim: sub")

        return payload
