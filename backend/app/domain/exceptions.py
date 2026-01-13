from uuid import UUID


class DomainError(Exception):
    """Base class for domain-specific errors."""

    pass


class UserIdNotFoundError(DomainError):
    """Raised when attempting to access a user by id that doesn't exist."""

    def __init__(self, user_id: UUID) -> None:
        self.user_id = user_id
        super().__init__(f"User with id {user_id} not found")


class UserEmailNotFoundError(DomainError):
    """Raised when attempting to access a user by email that doesn't exist."""

    def __init__(self, user_email: str) -> None:
        self.user_email = user_email
        super().__init__(f"User with email {user_email} not found")
