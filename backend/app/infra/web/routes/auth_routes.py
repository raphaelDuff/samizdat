from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def issue_token():
    # TODO: Use OAuth2PasswordRequestForm dependency here (FastAPI tutorial style).
    # TODO: Call AuthenticateUserUseCase + CreateAccessTokenUseCase.
    # TODO: Return TokenResponseModel (`access_token`, `token_type`).
    raise NotImplementedError


@router.get("/me")
async def read_me():
    # TODO: Add dependency for `get_current_active_user`.
    # TODO: Return current authenticated user view model.
    raise NotImplementedError
