from dataclasses import dataclass
from app.application.repositories.user_repository import UserRepository
from app.application.dtos.user_dtos import CreateUserRequestModel, UserResponseModel
from app.application.common.result import Result, Error
from app.domain.entities.user import User


@dataclass(frozen=True)
class CreatreUserCase:
    """
    Use case for registering a new user.
    It orchestrates persistence (Repository) and business rules (Domain Entity)
    """

    user_repository: UserRepository

    async def execute(self, request_model: CreateUserRequestModel) -> Result:
        """Execute the user creation process."""

        if await self.user_repository.get_by_email(request_model.email):
            return Result.failure(
                Error.business_rule_violation(
                    message=f"Email already registered: {request_model.email}"
                )
            )

        new_user = User(
            name=request_model.name,
            email=request_model.email,
            password_hash=request_model.password_hash,
            role=request_model.role,
            birth_date=request_model.birth_date,
        )

        await self.user_repository.save(new_user)
        return Result.sucess(UserResponseModel.from_entity(new_user))
