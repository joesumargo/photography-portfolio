from fastapi import APIRouter, HTTPException, Request

from app.router import templates

router = APIRouter()

ROMAN_NUMERALS = ["I.", "II.", "III.", "IV.", "V.", "VI."]

_PHOTO_NUMERALS = [
    "I", "II", "III", "IV", "V",
    "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV",
    "XVI", "XVII", "XVIII", "XIX", "XX",
]


def _build_toc_sections(gallery_service, active_slug: str | None = None) -> list[dict]:
    """Build TOC sections from collections, padded to 6 slots."""
    collections = gallery_service.list_collections()
    sections = []
    for i, numeral in enumerate(ROMAN_NUMERALS):
        if i < len(collections):
            c = collections[i]
            sections.append({
                "numeral": numeral,
                "label": c.title,
                "slug": c.slug,
                "active": c.slug == active_slug,
            })
        else:
            sections.append({
                "numeral": numeral,
                "label": f"Collection {numeral}",
                "slug": None,
                "active": False,
            })
    return sections


@router.get("/")
async def index(request: Request):
    gallery_service = request.app.state.gallery_service
    toc_sections = _build_toc_sections(gallery_service)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "toc_sections": toc_sections,
            "active_section": "cover",
        },
    )


@router.get("/{collection_slug}")
async def collection_page(request: Request, collection_slug: str):
    gallery_service = request.app.state.gallery_service
    collection = gallery_service.get_collection(collection_slug)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    toc_sections = _build_toc_sections(gallery_service, active_slug=collection_slug)
    photo_numerals = _PHOTO_NUMERALS[: len(collection.photos)]

    return templates.TemplateResponse(
        request=request,
        name="collection.html",
        context={
            "collection": collection,
            "toc_sections": toc_sections,
            "photo_numerals": photo_numerals,
            "active_section": collection_slug,
        },
    )
