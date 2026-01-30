from dataclasses import dataclass
from datetime import date
from app.application.use_cases.user_use_cases import CreateUserUseCase


@dataclass
class UserController:
    """Controller for user-related operations"""

    create_use_case: CreateUserUseCase

    def handle_create(
        self,
        name: str,
        email: str,
        password_hash: str,
        brith_date: date,
        role: str,
        is_active: bool,
    ):
        return "TODO: finish this controller"
