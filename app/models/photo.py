from datetime import date

from pydantic import BaseModel


class PhotoData(BaseModel):
    """A single photo with all its metadata."""

    id: str
    title: str
    description: str = ""
    date: date
    category: str
    location: str | None = None
    camera: str | None = None
    featured: bool = False

    # Computed URL fields (set by GalleryService)
    thumb_url: str = ""
    medium_url: str = ""
    full_url: str = ""
