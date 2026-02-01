from app.interfaces.presenters.base import UserPresenter
from app.application.dtos.user_dtos import UserResponseModel
from app.interfaces.view_models.user_vm import UserViewModel
from datetime import date


class WebUserPresenter(UserPresenter):
    """Web-specific user presenter."""

    def present_user(self, response_model: UserResponseModel) -> UserViewModel:
        """Format user for web display."""
        return UserViewModel(
            id=response_model.id,
            name=response_model.name,
            email=response_model.email,
            birth_date=self.format_birth_date(response_model.birth_date),
            role=response_model.role,
        )
