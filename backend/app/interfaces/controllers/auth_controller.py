from dataclasses import dataclass


@dataclass
class AuthController:
    # TODO: Inject auth use cases and a presenter/view-model mapper.
    # TODO: Keep framework-independent orchestration here.

    async def handle_token(self, username: str, password: str):
        # TODO: Orchestrate authenticate + token creation and return operation result.
        raise NotImplementedError

    async def handle_current_user(self, token: str):
        # TODO: Decode token, load user, and map to view model.
        raise NotImplementedError
