"""Interactive script to add a new photo to the portfolio.

Usage: uv run python scripts/new-photo.py [path/to/image.jpg]
"""

import shutil
import sys
from datetime import date
from pathlib import Path

import yaml
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PHOTOS_DIR = PROJECT_ROOT / "static" / "photos"
DATA_FILE = PROJECT_ROOT / "data" / "photos.yaml"

CATEGORIES = ["landscape", "cityscape", "portrait", "street", "nature", "other"]
SIZES = {"medium": 1200, "thumb": 600}
QUALITY = 85


def prompt(prompt_text: str, default: str = "") -> str:
    """Prompt for input with an optional default."""
    if default:
        response = input(f"{prompt_text} [{default}]: ").strip()
        return response if response else default
    return input(f"{prompt_text}: ").strip()


def prompt_choice(prompt_text: str, choices: list[str]) -> str:
    """Prompt user to pick from a list of choices."""
    print(f"{prompt_text}")
    for i, choice in enumerate(choices, 1):
        print(f"  {i}. {choice}")
    while True:
        raw = input("Choice (number or name): ").strip().lower()
        if raw.isdigit() and 1 <= int(raw) <= len(choices):
            return choices[int(raw) - 1]
        if raw in choices:
            return raw
        print(f"  Please pick 1-{len(choices)} or type a category name.")


def generate_thumbnails(photo_id: str, src_path: Path) -> None:
    """Generate medium and thumbnail versions of the source image."""
    img = Image.open(src_path)
    for size_name, max_dim in SIZES.items():
        dst_dir = PHOTOS_DIR / size_name
        dst_dir.mkdir(exist_ok=True)
        dst_path = dst_dir / f"{photo_id}.jpg"
        img_copy = img.copy()
        img_copy.thumbnail((max_dim, max_dim), Image.LANCZOS)

        save_kwargs: dict = {}
        exif = img.info.get("exif")
        if exif:
            save_kwargs["exif"] = exif

        img_copy.save(dst_path, quality=QUALITY, optimize=True, **save_kwargs)
        print(f"  Generated: {dst_path} ({img_copy.size[0]}×{img_copy.size[1]})")


def append_metadata(entry: dict) -> None:
    """Append a photo entry to data/photos.yaml."""
    if DATA_FILE.exists():
        data = yaml.safe_load(DATA_FILE.read_text()) or {}
    else:
        data = {}

    photos = data.get("photos", [])
    photos.append(entry)
    data["photos"] = photos

    yaml_text = yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)
    DATA_FILE.write_text(yaml_text)
    print(f"  Appended to {DATA_FILE}")


def main() -> None:
    # Accept image path as argument or prompt
    if len(sys.argv) > 1:
        image_path = Path(sys.argv[1]).expanduser().resolve()
    else:
        image_path = Path(prompt("Path to image file")).expanduser().resolve()

    if not image_path.exists():
        print(f"Error: file not found: {image_path}", file=sys.stderr)
        sys.exit(1)

    print(f"\nAdding photo: {image_path.name}\n")

    # Gather metadata
    default_id = image_path.stem.lower().replace(" ", "-").replace("_", "-")
    photo_id = prompt("Photo ID", default_id)
    title = prompt("Title", image_path.stem.replace("-", " ").replace("_", " ").title())
    description = prompt("Description", "")
    category = prompt_choice("Category", CATEGORIES)

    date_str = prompt("Date (YYYY-MM-DD)", date.today().isoformat())
    location = prompt("Location (optional)", "")
    camera = prompt("Camera / lens info (optional)", "")
    featured = prompt("Featured? [y/N]", "n").lower().startswith("y")

    # Copy full-resolution image
    full_dir = PHOTOS_DIR / "full"
    full_dir.mkdir(parents=True, exist_ok=True)
    dst_path = full_dir / f"{photo_id}.jpg"
    shutil.copy2(image_path, dst_path)
    print(f"\nCopied {image_path} → {dst_path}")

    # Generate thumbnails
    generate_thumbnails(photo_id, dst_path)

    # Append metadata
    entry: dict = {
        "id": photo_id,
        "title": title,
        "description": description,
        "date": date_str,
        "category": category,
        "featured": featured,
    }
    if location:
        entry["location"] = location
    if camera:
        entry["camera"] = camera

    append_metadata(entry)

    print(f"\n✓ Photo '{photo_id}' added. Refresh the gallery to see it.")


if __name__ == "__main__":
    main()
