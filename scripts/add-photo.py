"""Add photos to the portfolio from the command line.

Usage:
    uv run python scripts/add-photo.py import <image.jpg> --title "..." --category "..."
    uv run python scripts/add-photo.py generate-thumbnails
"""

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

from PIL import Image
from ruamel.yaml import YAML

ryaml = YAML()
ryaml.preserve_quotes = True
ryaml.width = 4096

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PHOTOS_DIR = PROJECT_ROOT / "static" / "photos"
PHOTOS_DATA = PROJECT_ROOT / "data" / "photos.yaml"
COLLECTIONS_DATA = PROJECT_ROOT / "data" / "collections.yaml"
SIZES = {"medium": 1200, "thumb": 600}
QUALITY = 85


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def generate_thumbnails(photo_id: str, src_path: Path) -> None:
    img = Image.open(src_path)
    for size_name, max_dim in SIZES.items():
        dst_dir = PHOTOS_DIR / size_name
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst_path = dst_dir / f"{photo_id}.jpg"
        img_copy = img.copy()
        img_copy.thumbnail((max_dim, max_dim), Image.LANCZOS)
        save_kwargs: dict = {}
        exif = img.info.get("exif")
        if exif:
            save_kwargs["exif"] = exif
        img_copy.save(dst_path, quality=QUALITY, optimize=True, **save_kwargs)
        print(f"  {size_name}: {dst_path} ({img_copy.size[0]}x{img_copy.size[1]})")


def append_metadata(entry: dict) -> None:
    if PHOTOS_DATA.exists():
        data = ryaml.load(PHOTOS_DATA.read_text())
    else:
        data = {}
    photos = data.setdefault("photos", [])
    photos.append(entry)
    ryaml.dump(data, PHOTOS_DATA)
    print(f"  Appended to {PHOTOS_DATA}")


def append_to_collection(photo_id: str, collection_slug: str) -> None:
    if not COLLECTIONS_DATA.exists():
        print(f"  Warning: {COLLECTIONS_DATA} not found, skipping collection update")
        return
    raw = ryaml.load(COLLECTIONS_DATA.read_text())
    collections = raw.get("collections", [])
    for c in collections:
        if c.get("slug") == collection_slug:
            if "photos" not in c:
                c["photos"] = []
            photos = c["photos"]
            if photo_id not in photos:
                photos.append(photo_id)
                c["photos"] = photos
                ryaml.dump(raw, COLLECTIONS_DATA)
                print(
                    f"  Added '{photo_id}' to collection "
                    f"'{collection_slug}' in {COLLECTIONS_DATA}"
                )
            else:
                print(f"  Photo '{photo_id}' already in collection '{collection_slug}'")
            return
    print(f"  Warning: collection '{collection_slug}' not found")


def cmd_import(args: argparse.Namespace) -> None:
    image_path = Path(args.image).expanduser().resolve()
    if not image_path.exists():
        print(f"Error: file not found: {image_path}", file=sys.stderr)
        sys.exit(1)

    photo_id = args.id or slugify(Path(image_path).stem)
    title = args.title
    category = args.category
    desc = args.description or ""
    photo_date = args.date or date.today().isoformat()
    location = args.location
    camera = args.camera
    featured = args.featured
    collection = args.collection

    if not title:
        print("Error: --title is required", file=sys.stderr)
        sys.exit(1)
    if not category:
        print("Error: --category is required", file=sys.stderr)
        sys.exit(1)

    print(f"Adding photo: {image_path.name}")
    print(f"  ID:       {photo_id}")
    print(f"  Title:    {title}")
    print(f"  Category: {category}")
    if collection:
        print(f"  Collection: {collection}")

    full_dir = PHOTOS_DIR / "full"
    full_dir.mkdir(parents=True, exist_ok=True)
    dst_path = full_dir / f"{photo_id}.jpg"
    if dst_path.exists():
        print(f"Error: {dst_path} already exists", file=sys.stderr)
        sys.exit(1)

    shutil.copy2(image_path, dst_path)
    print(f"  Copied -> {dst_path}")

    generate_thumbnails(photo_id, dst_path)

    entry: dict = {
        "id": photo_id,
        "title": title,
        "description": desc,
        "date": photo_date,
        "category": category,
        "featured": featured,
    }
    if location:
        entry["location"] = location
    if camera:
        entry["camera"] = camera
    append_metadata(entry)

    if collection:
        append_to_collection(photo_id, collection)

    print(f"\nDone. Photo '{photo_id}' added.")


def cmd_generate_thumbnails(args: argparse.Namespace) -> None:
    full_dir = PHOTOS_DIR / "full"
    if not full_dir.exists():
        print(f"Error: {full_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    image_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    images = sorted(f for f in full_dir.iterdir() if f.suffix.lower() in image_extensions)
    if not images:
        print(f"No images found in {full_dir}/")
        return

    generated, skipped = 0, 0
    for src in images:
        for size_name, max_dim in SIZES.items():
            dst_dir = PHOTOS_DIR / size_name
            dst = dst_dir / f"{src.stem}.jpg"
            if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
                skipped += 1
                continue
            dst_dir.mkdir(parents=True, exist_ok=True)
            img = Image.open(src)
            img.thumbnail((max_dim, max_dim), Image.LANCZOS)
            save_kwargs: dict = {}
            exif = img.info.get("exif")
            if exif:
                save_kwargs["exif"] = exif
            img.save(dst, quality=QUALITY, optimize=True, **save_kwargs)
            print(f"  {size_name}: {dst} ({img.size[0]}x{img.size[1]})")
            generated += 1

    print(f"\nDone: {generated} generated, {skipped} up to date.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Add photos to the photography portfolio")
    sub = parser.add_subparsers(dest="command")

    p_import = sub.add_parser("import", help="Import a new photo")
    p_import.add_argument("image", help="Path to the image file")
    p_import.add_argument("--title", "-t", required=True, help="Photo title")
    p_import.add_argument("--category", "-c", required=True, help="Photo category")
    p_import.add_argument("--id", help="Photo ID (default: slugified filename)")
    p_import.add_argument("--description", "-d", default="", help="Photo description")
    p_import.add_argument("--date", help="Date (YYYY-MM-DD, default: today)")
    p_import.add_argument("--location", "-l", help="Photo location")
    p_import.add_argument("--camera", help="Camera / lens info")
    p_import.add_argument("--featured", action="store_true", help="Mark as featured")
    p_import.add_argument("--collection", help="Collection slug to add photo to")

    help_text = "Generate missing medium/thumb versions for all photos"
    sub.add_parser("generate-thumbnails", help=help_text)

    args = parser.parse_args()

    if args.command == "import":
        cmd_import(args)
    elif args.command == "generate-thumbnails":
        cmd_generate_thumbnails(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
