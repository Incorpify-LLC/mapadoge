# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Training Material Generator built on CrewAI. Orchestrates 7 specialized agents to research a technical topic and produce a themed PowerPoint (`output/training_presentation.pptx`) and a Word reference manual (`output/reference_manual.docx`).

## Commands

- **Run**: `python main.py`
- **Run with custom topic**: `python main.py --topic "Zero Trust Architecture" --subpoints "Identity,Device Trust" --slides 15 --model ollama/deepseek-v4-pro:cloud`
- **Install deps**: `pip install -r requirements.txt`
- **System dependency**: Graphviz (`sudo apt-get install graphviz` or `brew install graphviz`)
- **Run tests**: `python -m pytest tests/ -v` (use `.venv/bin/python` in the project virtualenv)

## Architecture

### Sequential Agent Pipeline

`main.py` (`TrainingAppOrchestrator`) wires 7 agents and 7 tasks into a strict sequential `Crew` (`Process.sequential`). Each agent has exactly one task. The task context dependencies (`context=[...]`) are what actually drive the data flow — not all tasks run in pure order:

| Order | Agent | File | Task Context Dependencies |
|-------|-------|------|--------------------------|
| 1 | Librarian | `agents/librarian.py` | none |
| 2 | Researcher | `agents/researcher.py` | none |
| 3 | Scriptwriter | `agents/scriptwriter.py` | t1 (Librarian), t2 (Researcher) |
| 4 | Creative Director | `agents/creative_director.py` | none |
| 5 | Visual Architect | `agents/visual_architect.py` | t3 (Scriptwriter) |
| 6 | Visual Asset Manager | `agents/visual_asset_manager.py` | t3, t5 (Architect), t4 (Creative Director) |
| 7 | Compiler | `agents/compiler.py` | t3, t6 (Asset Manager) |

### Pydantic Model Flow

Tasks enforce structured output via `output_pydantic=ModelName` on the `Task` constructor. The models form a pipeline (`models.py`):

- `ResearchKB` — Researcher output (facts with implementation steps)
- `ContentScript` — Scriptwriter output (slides + manual sections). Task enforces `min_slides` (default 10) and requires every slide to have a unique `diagram_prompt`. Each `SlideContent` has a `layout_type` field (Title, Agenda, Title and Content, Diagram Full, Quote, Comparison, Divider) and multi-level `bullet_points` (List[BulletPoint] with `text` + `level` 0-3). `ManualSection` supports optional `custom_subheadings`.
- `StyleConfig` — Creative Director output (colors, fonts, theme name)
- `DesignSpecs` — Visual Architect output (maps every slide to a diagram path)
- `VisualPackage` — Visual Asset Manager output (final slide data with resolved image/diagram paths, preserves `layout_type`)

### Tool Registry

All tools use `@tool("name")` from `crewai.tools` and require a docstring. Each is registered per-agent in the factory's `tools=[...]` list:

| Tool | File | Registered On |
|------|------|---------------|
| `internet_search` | `tools/search_tools.py` | Librarian |
| `load_default_schema` | `tools/schema_loader.py` | Creative Director |
| `generate_infra_diagram` | `tools/diagram_tools.py` | Visual Architect, Visual Asset Manager |
| `generate_diagram_with_fallback` | `tools/diagram_tools.py` | Visual Architect |
| `validate_diagram_script` | `tools/diagram_tools.py` | Visual Architect |
| `fetch_technical_image` | `tools/image_tools.py` | Visual Asset Manager |
| `prepare_image_for_slide` | `tools/image_tools.py` | Visual Asset Manager |
| `create_final_ppt` | `tools/file_tools.py` | Compiler |
| `create_reference_doc` | `tools/file_tools.py` | Compiler |

### Theme System

`default_seed_schema.md` defines visual themes (default: "Corporate Deep Blue"). The parser (`tools/schema_loader.py`) extracts the **first** palette table and normalizes role names into `StyleConfig` fields: `primary` → `primary_color`, `secondary` → `secondary_color`, `accent` → `accent_color`, `background` → `background_color`. Two themes exist in the schema: "Corporate Deep Blue" and "Dark Modern".

### Diagram Fallback Chain

1. Visual Architect writes Python `diagrams` code; `tools/diagram_tools.py` saves it to `temp/`, runs it as a subprocess with a 120-second timeout
2. If the output PNG is missing or <100 bytes → returns `None`
3. `generate_diagram_with_fallback` then calls `fetch_technical_image` via DuckDuckGo image search
4. Visual Asset Manager verifies every slide has a valid asset and fetches fallback images for any missing diagrams

### LLM Resolution

Priority: `--model` CLI → `OLLAMA_MODEL` env → `GEMINI_API_KEY` env (auto-selects `gemini/gemini-2.5-flash`) → default `ollama/deepseek-v4-pro:cloud`.

Rate-limit fallback: if the primary model throws `429`, `resource_exhausted`, or `rate` in the error message, the app retries the full run with `--fallback-model` (default: `ollama/glm-5.1`).

## Code Conventions

- 4-space indentation
- `snake_case` for modules, functions, variables; `PascalCase` for Pydantic models and classes
- Import groups: stdlib, third-party, local (blank line between groups)
- Use type hints; Pydantic `Field(..., description="...")` for model field documentation
- Agent factories: `get_<role>(llm=...) -> crewai.Agent`
- Task factories: `get_<task>(agent, ...) -> crewai.Task`

## Configuration

- `config.yaml` (gitignored, user-local) overrides hardcoded defaults. Copy `config.yaml.example` to get started. CLI arguments always take precedence over config values. Resolution order: CLI > config.yaml > hardcoded fallback.
- Output files are versioned with a timestamp run ID: `training_presentation_20261019_143022.pptx` and a `run_metadata_*.json` sidecar capturing topic, model, theme, timestamp, and token usage metrics.
- Logging is configured via `tools/logging_config.py`. Set `LOG_LEVEL` env var (e.g. `DEBUG`) to control verbosity. All `print()` calls have been replaced with structured `logger.info/warning/error` calls.

## Key Implementation Details

- **Slide chunking** (`render_utils.py`): max 6 bullets per slide; overflow slides get `(N/M)` appended to the title
- **Slide layouts** (`render_utils.py`): `dispatch_slide_layout()` routes each slide to a renderer based on `layout_type` — Title (centered + subtitle + date), Agenda (numbered two-column), Diagram Full (large diagram + caption), Quote (pull-quote + attribution), Comparison (two-column), Divider (centered + accent bar), Title and Content (default with optional side image)
- **Multi-level bullets**: `apply_enhanced_ppt_style` respects `bullet.level` (0-3) for indented hierarchy
- **Search tools** (`search_tools.py`, `image_tools.py`) use DuckDuckGo (`ddgs`) with exponential backoff + jitter on 403/rate-limit errors
- **Legacy file**: `legacy/orchastration.py` is a 4-agent reference implementation — it is NOT imported by `main.py`
- **Pure utility modules**: `tools/render_utils.py` and `tools/schema_parser.py` have no crewai dependency and are unit-tested (38 tests)
- **Scratch files**: `tmp_writer/`, `tmp_agents.py` are gitignored experimental artifacts
- **Gitignored**: `output/`, `temp/`, `.env`, `__pycache__/`, `.venv/`, `config.yaml`
