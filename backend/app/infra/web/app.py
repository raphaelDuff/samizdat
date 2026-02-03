from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infra.config import Config
from app.infra.configuration.container import create_application
from app.infra.web.routes import user_routes
from app.interfaces.presenters.web.user_presenter import WebUserPresenter


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle - startup and shutdown.

    This is the composition root where concrete implementations
    are chosen and wired together.
    """
    # Startup: create container and attach to app state
    session_factory = Config.get_session_factory()
    app.state.container = create_application(
        session_factory=session_factory,
        user_presenter=WebUserPresenter(),  # Concrete choice at composition root
    )

    yield

    # Shutdown: cleanup resources
    await Config.dispose_engine()


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.

    :return: Web Backend Application
    :rtype: FastAPI
    """
    app = FastAPI(
        title="Samizdat",
        description="FastAPI with Domain Driven Design",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(user_routes.router)
    return app
