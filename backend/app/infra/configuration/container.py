"""
Application container that configures and wires together all components.

This container holds factories and shared dependencies.
The actual wiring is done by FastAPI's dependency injection system.
"""

from dataclasses import dataclass
from typing import Callable

from sqlmodel.ext.asyncio.session import AsyncSession

from app.interfaces.presenters.base import UserPresenter
from app.application.uow import UnitOfWork
from app.infra.repository_factory import create_repositories
from app.infra.uow import SqlAlchemyUnitOfWork


def create_application(
    session_factory: Callable[[], AsyncSession],
    user_presenter: UserPresenter,
) -> "Application":
    """
    Factory function for the Application container.

    Args:
        session_factory: Factory to create async database sessions
        user_presenter: Presenter for user-related output (injected from composition root)

    Returns:
        Configured Application instance with factories ready for DI
    """
    repo_factories = create_repositories()

    def uow_factory() -> UnitOfWork:
        return SqlAlchemyUnitOfWork(session_factory, repo_factories)

    return Application(
        uow_factory=uow_factory,
        user_presenter=user_presenter,
    )


@dataclass
class Application:
    """
    Application container that holds factories and shared dependencies.

    Unlike traditional containers that wire everything in __post_init__,
    this container provides factories that FastAPI's DI system uses
    to build request-scoped dependencies.
    """

    uow_factory: Callable[[], UnitOfWork]
    user_presenter: UserPresenter
