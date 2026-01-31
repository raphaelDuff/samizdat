from abc import ABC, abstractmethod
from app.application.dtos.user_dtos import UserResponseModel


class UserPresenter(ABC):
    """Abstract base presenter for user-related output"""

    @abstractmethod
    def present_user(self, user_response_model: UserResponseModel) -> UserViewModel
