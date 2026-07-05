from fastapi import APIRouter, HTTPException, Query, Request

from app.router import templates

router = APIRouter()


@router.get("/grid")
async def gallery_grid(request: Request, category: str = Query("all")):
    gallery_service = request.app.state.gallery_service
    photos = gallery_service.list_photos(category if category != "all" else None)
    return templates.TemplateResponse(
        request=request,
        name="partials/gallery_grid.html",
        context={"photos": photos, "active_category": category},
    )


@router.get("/photo/{photo_id}")
async def photo_lightbox(request: Request, photo_id: str):
    gallery_service = request.app.state.gallery_service
    photo = gallery_service.get_photo(photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return templates.TemplateResponse(
        request=request,
        name="partials/lightbox.html",
        context={"photo": photo},
    )
