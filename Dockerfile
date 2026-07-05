# ============================================================
# Stage 1: Builder — install Python dependencies via uv
# ============================================================
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies first (layer caching)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy source and install the project itself
COPY . .
RUN uv sync --frozen --no-dev

# ============================================================
# Stage 2: Tailwind CSS builder
# ============================================================
FROM node:20-alpine AS assets
WORKDIR /build
COPY tailwind.config.js ./
COPY styles/ styles/
RUN npx -y tailwindcss@3 -i styles/input.css -o output.css --minify

# ============================================================
# Stage 3: Runtime — minimal production image
# ============================================================
FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN groupadd -g 1000 app && useradd -u 1000 -g app -s /bin/sh -m app

# Copy virtualenv from builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy app code and data
COPY --from=builder /app/app /app/app
COPY --from=builder /app/data /app/data

# Copy compiled CSS
COPY --from=assets /build/output.css /app/static/css/output.css

# Copy photos and JS
COPY static/photos /app/static/photos
COPY static/js /app/static/js

EXPOSE 8000
USER app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
