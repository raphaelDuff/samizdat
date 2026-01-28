from fastapi import FastAPI


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.

    :return: Web Backend Application
    :rtype: FastAPI
    """
    app = FastAPI(
        title="Samizdat",
        description="FastAPI with Domain Drive Design",
        version="0.1.0",
    )

    # TODO: include routes
    return app
