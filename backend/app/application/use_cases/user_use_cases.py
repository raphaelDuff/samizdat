from dataclasses import dataclass

from app.application.common.result import Error, Result
from app.application.dtos.user_dtos import CreateUserRequestModel, UserResponseModel
from app.application.repositories.user_repository import UserRepository
from app.domain.entities.user import UserDomain
from uuid import uuid4
from infra.uow import UnitOfWork


@dataclass(frozen=True)
class CreatreUserCase:
    """
    Use case for registering a new user.
    It orchestrates persistence (Repository) and business rules (Domain Entity)
    """

    # user_repository: UserRepository

    uow: UnitOfWork

    async def execute(self, request_model: CreateUserRequestModel) -> Result:
        """Execute the user creation process."""
        async with self.uow:
            repo = self.uow.users

            if await self.user_repository.get_by_email(request_model.email):
                return Result.failure(
                    Error.business_rule_violation(
                        message=f"Email already registered: {request_model.email}"
                    )
                )

            new_user = UserDomain(
                id=uuid4(),
                name=request_model.name,
                email=request_model.email,
                password_hash=request_model.password_hash,
                role=request_model.role,
                birth_date=request_model.birth_date,
            )

            await self.user_repository.save(new_user)
            return Result.sucess(UserResponseModel.from_entity(new_user))
