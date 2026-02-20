from pydantic import BaseModel


class TokenViewModel(BaseModel):
    # TODO: Match API response contract used in auth_routes.
    # TODO: Typical fields:
    # TODO: - access_token: str
    # TODO: - token_type: str = "bearer"
    pass


class AuthErrorViewModel(BaseModel):
    # TODO: Standardize auth error response body and codes.
    # TODO: Keep shape consistent with your existing ErrorViewModel style.
    pass
