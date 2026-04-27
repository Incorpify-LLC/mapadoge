# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI Training Material Generator built on CrewAI. It orchestrates 7 specialized agents to research a technical topic and produce a themed PowerPoint presentation (`output/training_presentation.pptx`) and a Word reference manual (`output/reference_manual.docx`).

## Common Commands

- **Run the application**: `python main.py`
- **Run with custom topic**: `python main.py --topic "Zero Trust Architecture" --subpoints "Identity,Device Trust" --slides 15`
- **Install dependencies**: `pip install -r requirements.txt`
- **No test suite is configured.** If adding tests, prefer `pytest` in a top-level `tests/` directory.

## Prerequisites

- Python 3.10+
- Graphviz system dependency (`sudo apt-get install graphviz` or `brew install graphviz`)
- API credentials in a `.env` file: `GEMINI_API_KEY=...` or Ollama running locally/cloud

## Architecture

### Agent Pipeline (Sequential)

`main.py` (`TrainingAppOrchestrator`) wires 7 agents and 7 tasks in a strict sequential `Crew`:

1. **Librarian** (`agents/librarian.py`) → Synthesizes a master research document via web search (`tools/search_tools.py`).
2. **Researcher** (`agents/researcher.py`) → Deep-dive technical analysis on subpoints.
3. **Scriptwriter** (`agents/scriptwriter.py`) → Produces `ContentScript` (slides + manual sections). Task enforces a minimum slide count (`min_slides`, default 10) and requires every slide to have a unique `diagram_prompt`.
4. **Creative Director** (`agents/creative_director.py`) → Defines visual identity by parsing `default_seed_schema.md` (`tools/schema_loader.py`).
5. **Visual Architect** (`agents/visual_architect.py`) → Generates infrastructure diagrams using the `diagrams` library + Graphviz (`tools/diagram_tools.py`). Falls back to web image search if diagram generation fails.
6. **Visual Asset Manager** (`agents/visual_asset_manager.py`) → Coordinates and curates final visual assets.
7. **Compiler** (`agents/compiler.py`) → Assembles the final `.pptx` and `.docx` files (`tools/file_tools.py`).

### Data Flow

- Tasks pass context via `context=[...]` in CrewAI. `scripting_tasks.py` depends on both librarian and researcher outputs; `design_tasks.py` depends on scripting; `compilation_tasks.py` depends on scripting and visual assets.
- Structured outputs are enforced via Pydantic models in `models.py`: `ResearchKB`, `ContentScript`, `DesignSpecs`, `VisualPackage`.
- Theme data is loaded from `default_seed_schema.md` at runtime. The parser extracts the first palette table it finds and normalizes role names into `StyleConfig` fields (e.g., `primary` → `primary_color`).

### Key Files

| File | Purpose |
|------|---------|
| `main.py` | Entry point, argument parsing, LLM resolution, fallback logic, orchestrator instantiation |
| `models.py` | Pydantic models for structured agent outputs |
| `default_seed_schema.md` | Visual theme specification (colors, fonts, layout rules) |
| `orchastration.py` | Legacy 4-agent orchestration reference; not imported by `main.py` |

## Code Conventions

- 4-space indentation.
- `snake_case` for modules, functions, and variables; `PascalCase` for Pydantic models and classes.
- Imports grouped as: stdlib, third-party, local (blank line between groups).
- CrewAI tools must use the `@tool("tool_name")` decorator and include a docstring.
- Agent factories follow the pattern `get_<role>(llm=...) -> crewai.Agent`.
- Task factories follow the pattern `get_<task>(agent, ...) -> crewai.Task`.

## LLM Resolution & Fallback

`main.py` resolves the active LLM in this priority:
1. `--model` CLI argument
2. `OLLAMA_MODEL` environment variable
3. `GEMINI_API_KEY` environment variable (auto-selects `gemini/gemini-2.5-flash`)
4. Default: `ollama/deepseek-v4-pro:cloud`

If the primary model throws a rate-limit error (`429`, `resource_exhausted`, or `rate` in the error message), the app automatically retries with `--fallback-model` (default: `ollama/glm-5.1`).

## Adding Agents or Tools

- **New agent**: Create `agents/<role>.py` with a `get_<role>(llm=...)` factory, then register it in `TrainingAppOrchestrator.__init__` in `main.py`.
- **New tool**: Define the function in the appropriate `tools/*.py` file, decorate with `@tool("name")`, add a docstring, and register it in the relevant agent's `tools=[...]` list.

## Important Implementation Details

- `tools/diagram_tools.py` writes diagram scripts to `temp/` and executes them as subprocesses with a 120-second timeout. If the output PNG is missing or <100 bytes, it returns `None` to trigger fallback behavior.
- `tools/search_tools.py` and `tools/image_tools.py` use DuckDuckGo (`ddgs`) with exponential backoff and jitter on 403/rate-limit errors.
- `tools/file_tools.py` chunks slides into max 6 bullets per slide, appending `(N/M)` to titles when splitting.
- Generated artifacts in `output/` and intermediate files in `temp/` are gitignored.
