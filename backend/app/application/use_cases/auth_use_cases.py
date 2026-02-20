from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticateUserUseCase:
    # TODO: Inject dependencies:
    # TODO: - user repository access (through UnitOfWork or dedicated repository)
    # TODO: - password verification service
    # TODO: Return your existing Result type with domain/application error mapping.
    async def execute(self, username: str, password: str):
        # TODO: 1) Load user by email/username
        # TODO: 2) Verify password hash
        # TODO: 3) Check active/disabled flags
        # TODO: 4) Return authenticated user (or failure)
        raise NotImplementedError


@dataclass(frozen=True)
class CreateAccessTokenUseCase:
    # TODO: Inject JWT service and auth settings (expiry, algorithm, secret key).
    async def execute(self, subject: str, role: str | None = None):
        # TODO: Build JWT claims (`sub`, `exp`, and optional role/scopes).
        # TODO: Return token response DTO or Result wrapper.
        raise NotImplementedError
