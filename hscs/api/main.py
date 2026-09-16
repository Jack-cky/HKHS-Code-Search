from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import health, search
from .services import get_engine


def create_app() -> FastAPI:
    app = FastAPI(title="HKHS Code Search")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_methods=["GET"],
    )

    for router in [health, search]:
        app.include_router(router.router, prefix="/api/v1")

    get_engine()

    return app


app = create_app()
