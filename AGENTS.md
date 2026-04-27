# Repository Guidelines

## Project Structure & Module Organization

- `main.py` — Application entry point. Initializes the CrewAI workflow.
- `orchastration.py` — Orchestration logic for coordinating agents.
- `models.py` — Pydantic data models defining structured outputs.
- `agents/` — Agent definitions. Each module exports a factory (e.g., `get_researcher()`).
- `tasks/` — Task definitions mapped to agents (e.g., `research_tasks.py`).
- `tools/` — Shared utilities: `diagram_tools.py`, `file_tools.py`, `image_tools.py`, `search_tools.py`.
- `output/` — Generated artifacts (documents, presentations).
- `temp/` — Intermediate image assets and diagram scripts.

## Build, Test, and Development Commands

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

No test suite or build script is currently configured.

## Coding Style & Naming Conventions

- **Indentation:** 4 spaces.
- **Naming:** `snake_case` for modules, functions, and variables; `PascalCase` for Pydantic models and classes.
- **Imports:** Group standard library, third-party, and local imports with a blank line between groups.
- **Typing:** Use type hints and Pydantic `BaseModel` for structured data.
- **Docstrings:** Prefer Pydantic `Field(..., description="...")` for model field documentation.

## Testing Guidelines

No tests exist yet. If adding tests, prefer `pytest` and place them in a top-level `tests/` directory mirroring the package structure.

## Commit & Pull Request Guidelines

- Use imperative mood in commit messages (e.g., `Add diagram caching tool`).
- Keep commits focused on a single logical change.
- Include a brief description and any relevant context in pull requests.

## Security & Configuration Tips

- Store API keys and secrets in a `.env` file. The project loads environment variables via `python-dotenv`.
- Do not commit credentials or generated artifacts in `output/` and `temp/` to version control.
