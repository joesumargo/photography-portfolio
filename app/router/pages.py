from fastapi import APIRouter, Request

from app.router import templates

router = APIRouter()


@router.get("/")
async def index(request: Request):
    gallery_service = request.app.state.gallery_service
    photos = gallery_service.list_photos()
    categories = gallery_service.categories
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "photos": photos,
            "categories": categories,
            "active_category": "all",
        },
    )
