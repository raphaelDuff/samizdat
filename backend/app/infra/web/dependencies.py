"""
FastAPI Dependency Injection graph.

This module defines the dependency injection chain for the application.
Each dependency function explicitly declares its dependencies, making the
dependency graph clear and testable.
"""

from typing import Callable

from fastapi import Depends, Request

from app.application.uow import UnitOfWork
from app.application.use_cases.user_use_cases import CreateUserUseCase, GetUsersUseCase
from app.infra.configuration.container import Application
from app.interfaces.controllers.user_controller import UserController
from app.interfaces.presenters.base import UserPresenter


def get_container(request: Request) -> Application:
    """
    Get the application container from request state.

    The container is attached to app.state during application startup
    via the lifespan context manager.
    """
    return request.app.state.container


def get_user_presenter(
    container: Application = Depends(get_container),
) -> UserPresenter:
    """Get the user presenter from the container."""
    return container.user_presenter


def get_uow_factory(
    container: Application = Depends(get_container),
) -> Callable[[], UnitOfWork]:
    """Get the UnitOfWork factory from the container."""
    return container.uow_factory


def get_create_user_use_case(
    uow_factory: Callable[[], UnitOfWork] = Depends(get_uow_factory),
) -> CreateUserUseCase:
    """
    Create a CreateUserUseCase with a fresh UoW.

    Each request gets its own UoW instance, ensuring proper
    transaction isolation between requests.
    """
    return CreateUserUseCase(uow=uow_factory())


def get_get_users_use_case(
    uow_factory: Callable[[], UnitOfWork] = Depends(get_uow_factory),
) -> GetUsersUseCase:
    """Create a GetUsersUseCase with a fresh UoW."""
    return GetUsersUseCase(uow=uow_factory())


def get_user_controller(
    create_use_case: CreateUserUseCase = Depends(get_create_user_use_case),
    presenter: UserPresenter = Depends(get_user_presenter),
) -> UserController:
    """
    Build the UserController with all its dependencies.

    This is the main entry point for user-related route handlers.
    Each request gets a fresh controller with request-scoped dependencies.
    """
    return UserController(
        create_use_case=create_use_case,
        presenter=presenter,
    )
