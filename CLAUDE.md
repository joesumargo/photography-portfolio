# CLAUDE.md

## Project Intent

This is a **professional photography portfolio** — a bespoke website to showcase the owner's photography work to potential clients and the wider photo community. It's a long-term project meant to eventually become a polished, feature-complete site the owner is proud to share publicly.

But the portfolio is also a **learning vehicle**. The owner is using this project to deeply understand modern web development, with particular emphasis on:

- **CI/CD pipelines** — automated testing, container image builds, deployment automation
- **Docker & containers** — multi-stage builds, image optimization, production container patterns
- **Full-stack integration** — how the frontend, backend, build tools, and deployment pipeline fit together

The journey matters as much as the destination.

## Audience & Tone

- **Primary audience**: Potential clients and collaborators evaluating the photographer's work
- **Secondary**: Fellow photographers, the broader creative community
- The site should feel **professional, design-forward, and intentional** — the presentation of the work should reflect the quality of the work itself
- Visual impact first, words second

## Architecture Philosophy

**Start simple, but don't box ourselves in.** The current architecture (FastAPI + Jinja2 + HTMX + YAML flat files) is intentionally minimal. It's the right foundation, but we expect to evolve:

- YAML metadata may grow into a database when photo volume or querying needs increase
- An admin panel or CMS may be added when manual YAML editing becomes tedious
- Auth may be added for client galleries or protected content
- The UI will be iterated on significantly — the current templates are a functional scaffold

**No premature complexity, but no dead ends either.** When making architectural decisions, prefer approaches that leave the door open for future growth without over-engineering the present.

## Design Approach

- **Minimalist, dark aesthetic** — let the photos dominate
- **UI is iterative** — the current templates are bare scaffolding. Expect many passes on typography, spacing, transitions, and layout before it feels right
- **Responsive by default** — the site must look excellent on mobile, tablet, and desktop
- **Performance-conscious** — pre-generated thumbnails, lazy loading, minimal JavaScript

## Development Practices

- Package management with `uv` (Python 3.12+)
- Linting with `ruff`, type-checking with `mypy`
- Tests with `pytest` (currently 8 tests covering routes and HTMX endpoints)
- Tailwind CSS via standalone CLI (no Node.js required locally)
- `make dev` for the dev loop, `make ci` for pre-push checks
- Docker multi-stage builds for production images

## Key Constraints

- **CI/CD is the owner's domain** — they want to build the pipeline themselves as a learning exercise. Don't set up GitHub Actions or deployment automation unless explicitly asked
- **No database yet** — everything is flat files (YAML for metadata, static images on disk)
- **Keep it runnable** — `make dev` should always work. Every change should preserve the ability to start the server, run tests, and build the Docker image

## Future Direction

- UI polish passes (typography, transitions, gallery layouts, lightbox behavior)
- CI/CD pipeline (owner-built)
- Deployment to a cloud platform (TBD — Docker makes this flexible)
- Photo management improvements as the collection grows
- Possible: blog, client galleries, contact form, search
