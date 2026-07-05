from fastapi import APIRouter, Request

from app.router import templates

router = APIRouter()

TOC_SECTIONS = [
    {"numeral": "I.",   "label": "Collection One"},
    {"numeral": "II.",  "label": "Collection Two"},
    {"numeral": "III.", "label": "Collection Three"},
    {"numeral": "IV.",  "label": "Collection Four"},
    {"numeral": "V.",   "label": "Collection Five"},
    {"numeral": "VI.",  "label": "Collection Six"},
]


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "toc_sections": TOC_SECTIONS,
        },
    )
