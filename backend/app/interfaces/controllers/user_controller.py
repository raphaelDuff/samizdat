from dataclasses import dataclass
from datetime import date
from app.application.use_cases.user_use_cases import CreateUserUseCase
from app.interfaces.view_models.base import OperationResult
from app.application.dtos.user_dtos import CreateUserRequestModel


@dataclass
class UserController:
    """Controller for user-related operations"""

    create_use_case: CreateUserUseCase

    async def handle_create(
        self,
        name: str,
        email: str,
        password_hash: str,
        brith_date: date,
        role: str,
        is_active: bool,
    ) -> OperationResult:
        try:
            request = CreateUserRequestModel(
                name=name,
                email=email,
                password_hash=password_hash,
                birth_date=brith_date,
                role=role,
                is_active=is_active,
            )
            result = await self.create_use_case.execute(request)
            if result.is_success:
                # TODO: Create the presenter
                view_model = self
            
        except ValueError as e:
            #TODO
        return "TODO: finish this controller"
