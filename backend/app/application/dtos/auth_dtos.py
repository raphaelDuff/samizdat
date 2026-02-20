from pydantic import BaseModel


class TokenResponseModel(BaseModel):
    # TODO: Keep FastAPI tutorial compatibility:
    # TODO: add `access_token: str` and `token_type: str` (usually "bearer").
    pass


class LoginRequestModel(BaseModel):
    # TODO: For `/token` with OAuth2PasswordRequestForm, you may not use this DTO directly.
    # TODO: If you also expose JSON login, add `email_or_username` and `password` fields.
    pass
