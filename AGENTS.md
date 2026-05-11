# AGENTS.md — Guidance for AI coding agents

Purpose: short, actionable guidance for coding agents working in this repository.

Quick facts
- **Python:** >= 3.13 (see [pyproject.toml](pyproject.toml)).
- **Run app:** `uvicorn app.main:app --reload` (see [app/main.py](app/main.py)).
- **Docker:** `docker-compose up -d` (see [docker-compose.yml](docker-compose.yml)).
- **Migrations:** `alembic upgrade head` (see [alembic.ini](alembic.ini) and `alembic/`).
- **Tests:** `pytest` (configuration in [pyproject.toml](pyproject.toml); tests under `app/tests`).

What agents should know (concise)
- Use the project's README for onboarding steps and environment setup: [README.md](README.md).
- Dependencies are declared in `pyproject.toml`; dev extras include `pytest`, `pytest-asyncio`, `pytest-xdist`, and `ruff`.
- Tests create temporary databases (see `app/tests/conftest.py`) and rely on `docker-compose` for a PostgreSQL service when needed.
- The app entrypoint is `app.main:app`; routers are in `app/api`.
- Alembic is configured for async SQLAlchemy—use the repository's alembic folder for migrations.

Agent behavior recommendations
- Prefer linking to existing docs instead of copying long sections; follow "link, don't embed".
- When suggesting code edits, reference the exact file(s) and include minimal, focused patches.
- Run tests locally with `pytest -q` and use `-k` to target changed areas during iteration.
- Respect the project's Python version and typing/mypy strictness.

Next customizations to consider
- Add a small `.github/copilot-instructions.md` if repository owners want per-repo agent role presets.
- Create a `/.vscode` or `devcontainer` quickstart note for reproducible developer environments.

Relevant files
- [README.md](README.md)
- [pyproject.toml](pyproject.toml)
- [app/main.py](app/main.py)
- [alembic.ini](alembic.ini)
- [app/tests/conftest.py](app/tests/conftest.py)
