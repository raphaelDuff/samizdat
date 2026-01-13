from uuid import UUID

from app.application.repositories.user_repository import UserRepository
from app.domain.entities.user import User
from app.domain.exceptions import UserEmailNotFoundError, UserIdNotFoundError
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import Sequence


class PostgresRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        """
        Initialize repository with async database session.

        Args:
            session: SQLModel async session for database operations
        """
        self._session = session

    async def get(self, user_id: UUID) -> User:
        """
        Retrieve a user by ID.

        Args:
            user_id: The unique identifier of the user

        Returns:
            User entity

        Raises:
            UserNotFoundError: If user doesn't exist
        """
        user = await self._session.get(User, user_id)
        if user is None:
            raise UserIdNotFoundError(user_id)
        return user

    async def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by email address.

        Args:
            email: The email address of the user

        Returns:
            User entity

        Raises:
            UserEmailNotFoundError: If user with the email doesn't exist
        """
        statement = select(User).where(User.email == email)
        result = await self._session.exec(statement)
        user = result.first()
        if user is None:
            raise UserEmailNotFoundError(email)
        return user

    async def get_all(self) -> Sequence[User]:
        """
        Retrieve all users from the database.

        Returns:
            Sequence of all User entities
        """
        statement = select(User)
        result = await self._session.exec(statement)
        users = result.all()
        return users

    async def save(self, user: User) -> None:
        """
        Save a user to the database.

        Args:
            user: The User entity to save
        """
        # TODO - create db model and a mapper
        # model = to_model(user)
        self._session.add(user)
        # TODO - modify to use Unit of work
        await self._session.commit()

    # TODO - Create the missing methods
