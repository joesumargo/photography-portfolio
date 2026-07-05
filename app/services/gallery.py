from pathlib import Path

import yaml

from app.models.photo import PhotoData


class GalleryService:
    """Loads and serves photo metadata from a YAML file."""

    def __init__(self, data_path: Path, photos_base_url: str) -> None:
        self.data_path = data_path
        self.photos_base_url = photos_base_url
        self._photos: list[PhotoData] = []
        self._categories: list[str] = []

    def load(self) -> None:
        """Load photo metadata from the YAML file. Called once at startup."""
        if not self.data_path.exists():
            self._photos = []
            self._categories = []
            return

        raw = yaml.safe_load(self.data_path.read_text()) or {}
        self._photos = [
            PhotoData(
                id=p["id"],
                title=p["title"],
                description=p.get("description", ""),
                date=p["date"],
                category=p["category"],
                location=p.get("location"),
                camera=p.get("camera"),
                featured=p.get("featured", False),
                thumb_url=f"{self.photos_base_url}/thumb/{p['id']}.jpg",
                medium_url=f"{self.photos_base_url}/medium/{p['id']}.jpg",
                full_url=f"{self.photos_base_url}/full/{p['id']}.jpg",
            )
            for p in raw.get("photos", [])
        ]
        self._photos.sort(key=lambda p: p.date, reverse=True)
        self._categories = sorted({p.category for p in self._photos})

    def list_photos(self, category: str | None = None) -> list[PhotoData]:
        """Return all photos, optionally filtered by category."""
        if category and category != "all":
            return [p for p in self._photos if p.category == category]
        return list(self._photos)

    def get_photo(self, photo_id: str) -> PhotoData | None:
        """Look up a single photo by its id."""
        for p in self._photos:
            if p.id == photo_id:
                return p
        return None

    @property
    def categories(self) -> list[str]:
        return self._categories
