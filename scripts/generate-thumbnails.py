"""Generate medium and thumbnail versions of all photos in static/photos/full/.

Usage: uv run python scripts/generate-thumbnails.py [--dry-run]
"""

import argparse
import sys
from pathlib import Path

from PIL import Image

SIZES = {
    "medium": 1200,
    "thumb": 600,
}

QUALITY = 85


def generate(source_dir: Path, dry_run: bool = False) -> None:
    if not source_dir.exists():
        print(f"Error: source directory '{source_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    image_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    images = sorted(
        f
        for f in source_dir.iterdir()
        if f.suffix.lower() in image_extensions
    )

    if not images:
        print(f"No images found in {source_dir}/")
        return

    processed, up_to_date = 0, 0

    for src_path in images:
        for size_name, max_dim in SIZES.items():
            dst_dir = source_dir.parent / size_name
            dst_path = dst_dir / src_path.name

            # Check if target is already up to date
            if dst_path.exists():
                src_mtime = src_path.stat().st_mtime
                dst_mtime = dst_path.stat().st_mtime
                if dst_mtime >= src_mtime:
                    up_to_date += 1
                    continue

            if dry_run:
                print(f"Would generate: {dst_path} ({max_dim}px)")
                processed += 1
                continue

            dst_dir.mkdir(exist_ok=True)
            img = Image.open(src_path)
            img.thumbnail((max_dim, max_dim), Image.LANCZOS)

            # Preserve EXIF orientation if present
            save_kwargs: dict = {}
            exif = img.info.get("exif")
            if exif:
                save_kwargs["exif"] = exif

            img.save(dst_path, quality=QUALITY, optimize=True, **save_kwargs)
            print(f"  Generated: {dst_path} ({img.size[0]}×{img.size[1]})")
            processed += 1

    if dry_run:
        print(f"\nDry run: {processed} would be generated, {up_to_date} already up to date.")
    else:
        print(f"\nDone: {processed} generated, {up_to_date} already up to date.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate photo thumbnails")
    parser.add_argument(
        "--source-dir",
        default="static/photos/full",
        help="Directory containing full-resolution images (default: static/photos/full)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without doing it",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    source_dir = project_root / args.source_dir
    generate(source_dir, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
