from fastapi import APIRouter, HTTPException, Request

from app.router import templates

router = APIRouter()

ROMAN_NUMERALS = ["I.", "II.", "III.", "IV.", "V.", "VI."]


def _build_toc_sections(gallery_service) -> list[dict]:
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
            })
        else:
            sections.append({
                "numeral": numeral,
                "label": f"Collection {numeral}",
                "slug": None,
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
        },
    )


@router.get("/{collection_slug}")
async def collection_page(request: Request, collection_slug: str):
    gallery_service = request.app.state.gallery_service
    collection = gallery_service.get_collection(collection_slug)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    toc_sections = _build_toc_sections(gallery_service)
    photo_numerals = ["I", "II", "III", "IV", "V"]

    return templates.TemplateResponse(
        request=request,
        name="collection.html",
        context={
            "collection": collection,
            "toc_sections": toc_sections,
            "photo_numerals": photo_numerals,
        },
    )
