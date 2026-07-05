# photography-portfolio

A minimalist, bespoke photography portfolio website built with FastAPI, HTMX, and Tailwind CSS.

## Tech Stack

| Layer | Choice |
|-------|--------|
| Backend | FastAPI + Jinja2 |
| Interactivity | HTMX 2.x (server-driven partials) |
| CSS | Tailwind CSS 3 (standalone CLI) |
| Image processing | Pillow (pre-generated thumbnails) |
| Photo metadata | YAML (human-editable, git-tracked) |
| Container | Docker (3-stage multi-stage build) |
| Package manager | uv |
| Dev tools | pytest, ruff, mypy |

## Project Structure

```
├── app/
│   ├── main.py                    # FastAPI app factory + lifespan
│   ├── config.py                  # Pydantic Settings (env-based)
│   ├── router/
│   │   ├── pages.py               # Full-page routes (GET /)
│   │   └── htmx.py                # HTMX partials (/grid, /photo/{id})
│   ├── models/
│   │   └── photo.py               # PhotoData model
│   ├── services/
│   │   └── gallery.py             # YAML loader, filtering, categories
│   └── templates/
│       ├── base.html              # Shell: doctype, meta, nav
│       ├── index.html             # Full gallery page
│       └── partials/
│           ├── gallery_grid.html  # Photo grid (HTMX target)
│           └── lightbox.html      # Lightbox overlay content
├── static/
│   ├── css/output.css             # Compiled Tailwind
│   ├── js/app.js                  # Lightbox close + escape key
│   └── photos/
│       ├── full/                  # Full-resolution (2400px)
│       ├── medium/                # Lightbox size (1200px)
│       └── thumb/                 # Grid thumbnails (600px)
├── data/
│   └── photos.yaml               # All photo metadata
├── styles/
│   └── input.css                  # Tailwind source
├── scripts/
│   ├── generate-thumbnails.py     # Pillow: full → medium + thumb
│   └── new-photo.py              # Interactive: add a photo end-to-end
├── tests/
│   ├── conftest.py                # Test fixtures
│   ├── test_data/photos.yaml     # Test data (2 photos)
│   ├── test_pages.py              # Page route tests
│   └── test_htmx.py               # HTMX endpoint tests
├── Dockerfile                      # 3-stage multi-stage build
├── Makefile                        # dev, test, lint, tailwind, docker-build
├── pyproject.toml
└── tailwind.config.js
```

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Docker (for containerized deployment)

### Setup

```bash
# Clone the repo
git clone git@github.com:joesumargo/photography-portfolio.git
cd photography-portfolio

# Install dependencies
uv sync
uv sync --extra dev

# Download Tailwind standalone CLI (macOS ARM)
curl -sL https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.17/tailwindcss-macos-arm64 -o tailwindcss
chmod +x tailwindcss

# Build CSS
make tailwind

# Start dev server
make dev
```

Visit `http://localhost:8000` — the gallery loads with sample photos.

API docs at `http://localhost:8000/docs`.

## Makefile Commands

| Command | What it does |
|---------|-------------|
| `make dev` | Start dev server with hot reload |
| `make test` | Run pytest (8 tests) |
| `make lint` | Run ruff + mypy |
| `make format` | Auto-format with ruff |
| `make tailwind` | Compile Tailwind CSS for production |
| `make tailwind-watch` | Watch for CSS changes |
| `make thumbnails` | Generate medium + thumb from full/ |
| `make new-photo` | Interactive: add a new photo |
| `make docker-build` | Build Docker image |
| `make docker-run` | Run Docker image locally |
| `make ci` | Run full CI check (lint + test + tailwind) |
| `make clean` | Remove build artifacts |

## Routes

| Method | Path | Response | Purpose |
|--------|------|----------|---------|
| GET | `/` | Full HTML page | Gallery with all photos |
| GET | `/grid?category=X` | HTML partial | HTMX: filter gallery by category |
| GET | `/photo/{id}` | HTML partial | HTMX: load lightbox for a photo |
| Static | `/static/*` | Static files | CSS, JS, all image sizes |

## Adding a Photo

**Option A — Interactive script:**
```bash
make new-photo
# Follow the prompts: image path, title, category, etc.
```

**Option B — Manual:**
1. Copy image to `static/photos/full/`
2. Run `make thumbnails` to generate medium and thumb versions
3. Add an entry to `data/photos.yaml`:
```yaml
- id: "my-photo"
  title: "My Photo"
  description: "A beautiful shot."
  date: "2025-07-04"
  category: "landscape"
  location: "Somewhere"
  camera: "Sony A7 IV"
  featured: false
```

## Photo Metadata Format

```yaml
photos:
  - id: "mountain-sunset"          # unique slug, also the filename
    title: "Mountain Sunset"
    description: "Golden hour light over the range."
    date: "2025-08-15"             # YYYY-MM-DD
    category: "landscape"          # used for filtering
    location: "Sierra Nevada, CA"  # optional
    camera: "Sony A7 IV"           # optional
    featured: true                 # optional
```

Photo files follow the convention: `static/photos/{size}/{id}.jpg`

## Docker

Multi-stage build (builder → Tailwind assets → slim runtime):

```bash
make docker-build       # Build the image
make docker-run         # Run on port 8000
```

The image is ~150-200MB and runs as a non-root user.

## Configuration

Environment variables (via `.env` file or shell):

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_TITLE` | Photography Portfolio | Site title |
| `APP_DEBUG` | false | Enable debug mode |
| `APP_PHOTOS_DATA_PATH` | data/photos.yaml | Path to metadata file |
| `APP_PHOTOS_BASE_URL` | /static/photos | Base URL for photo files |

Copy `.env.example` to `.env` to customize.

## CI/CD

CI/CD pipeline is intentionally left for you to build as a learning exercise. The project is ready for it:
- `make ci` runs the full local check (lint + test + build)
- The Dockerfile is platform-agnostic
- Consider starting with a GitHub Actions workflow that runs lint → test → docker build

## License

Private project.
