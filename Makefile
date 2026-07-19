.PHONY: dev tailwind test lint clean docker-build ci

# Install all dependencies
install:
	uv sync
	uv sync --extra dev

# Local dev server with hot reload
dev:
	@echo "Starting dev server at http://localhost:8000..."
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Build Tailwind CSS (production)
tailwind:
	./tailwindcss -i styles/input.css -o static/css/output.css --minify

# Build Tailwind CSS and watch for changes
tailwind-watch:
	./tailwindcss -i styles/input.css -o static/css/output.css --watch

# Run tests
test:
	uv run pytest -v

# Lint and type-check
lint:
	uv run ruff check app/ tests/ scripts/
	uv run mypy app/

# Format code
format:
	uv run ruff format app/ tests/ scripts/

# Add a new photo (non-interactive CLI)
add-photo:
	uv run python scripts/add-photo.py

# Generate thumbnails
thumbnails:
	uv run python scripts/generate-thumbnails.py

# Add a new photo (interactive)
new-photo:
	uv run python scripts/new-photo.py

# Build Docker image
docker-build:
	docker build -t photography-portfolio:latest .

# Run Docker image locally
docker-run:
	docker run --rm -p 8000:8000 photography-portfolio:latest

# Full CI check (lint + test + tailwind)
ci: lint test tailwind
	@echo "All checks passed!"

# Clean build artifacts
clean:
	rm -f static/css/output.css
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
