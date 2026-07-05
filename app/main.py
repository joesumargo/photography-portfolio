from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.services.gallery import GalleryService


def create_app(
    photos_data_path: Path | None = None,
    photos_base_url: str | None = None,
) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        photos_data_path: Override path to photos.yaml (for testing).
        photos_base_url: Override base URL for photo files.
    """
    data_path = photos_data_path or Path(settings.photos_data_path)
    base_url = photos_base_url or settings.photos_base_url

    gallery_service = GalleryService(
        data_path=data_path,
        photos_base_url=base_url,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Load gallery data on startup."""
        gallery_service.load()
        yield

    app = FastAPI(title=settings.title, debug=settings.debug, lifespan=lifespan)

    # Mount static files
    static_dir = Path("static")
    static_dir.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Register routers
    from app.router.htmx import router as htmx_router
    from app.router.pages import router as pages_router

    app.include_router(pages_router)
    app.include_router(htmx_router)

    # Store gallery service reference for routers to use
    app.state.gallery_service = gallery_service

    return app


# Module-level singleton for production
app = create_app()
