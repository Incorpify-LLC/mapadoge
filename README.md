# AI Training Material Generator

A multi-agent CrewAI application that automatically researches technical topics and generates professional PowerPoint presentations and reference manuals.

## Overview

This project uses a crew of specialized AI agents to:

1. **Research** technical topics using web search and internal knowledge
2. **Synthesize** findings into structured knowledge bases
3. **Script** slide content and detailed reference manuals
4. **Design** visual identities with themed color palettes
5. **Generate** infrastructure diagrams using Python diagrams + Graphviz
6. **Compile** everything into polished `.pptx` and `.docx` files

## Features

- **Automated Research**: Deep-dive technical analysis with implementation steps and troubleshooting
- **Professional PPT Generation**: Themed slides with accent bars, headers, footers, and slide numbers
- **Diagram Support**: Infrastructure diagrams via `diagrams` library; automatic fallback to web images
- **Visual Identity**: Default seed schema with Corporate Deep Blue theme; customizable palettes
- **Reference Manuals**: Detailed technical documents with structured sections
- **Multi-Agent Pipeline**: 7 specialized agents working sequentially via CrewAI

## Architecture

```
main.py
├── Librarian Agent          # Research synthesis
├── Researcher Agent         # Technical deep-dive
├── Scriptwriter Agent       # Content scripting
├── Creative Director Agent  # Visual identity & theming
├── Visual Architect Agent   # Diagram generation
├── Visual Asset Manager     # Image fallback & curation
└── Compiler Agent           # PPT/DOCX assembly
```

## Project Structure

```
.
├── main.py                    # Application entry point
├── models.py                  # Pydantic data models
├── orchastration.py           # Legacy orchestration reference
├── default_seed_schema.md     # Default visual theme specification
├── requirements.txt           # Python dependencies
├── agents/                    # Agent definitions
│   ├── compiler.py
│   ├── creative_director.py
│   ├── librarian.py
│   ├── researcher.py
│   ├── scriptwriter.py
│   ├── visual_architect.py
│   └── visual_asset_manager.py
├── tasks/                     # Task definitions
│   ├── compilation_tasks.py
│   ├── design_tasks.py
│   ├── librarian_tasks.py
│   ├── research_tasks.py
│   ├── scripting_tasks.py
│   ├── style_tasks.py
│   └── visual_tasks.py
├── tools/                     # Agent tools
│   ├── diagram_tools.py       # Diagram generation + validation
│   ├── file_tools.py          # PPT/DOCX creation
│   ├── image_tools.py         # Image search & preparation
│   ├── schema_loader.py       # Seed schema parser
│   └── search_tools.py        # Web search
├── output/                    # Generated artifacts (gitignored)
└── temp/                      # Intermediate assets (gitignored)
```

## Prerequisites

- Python 3.10+
- [Graphviz](https://graphviz.org/download/) (system dependency for `diagrams`)
- Gemini API key

## Setup

1. **Clone the repository**

```bash
git clone <repo-url>
cd <repo-directory>
```

2. **Create a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scriptsctivate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

5. **Install Graphviz (system dependency)**

- **Ubuntu/Debian**: `sudo apt-get install graphviz`
- **macOS**: `brew install graphviz`
- **Windows**: Download from [graphviz.org](https://graphviz.org/download/)

## Usage

### Basic Usage (with defaults)

```bash
python main.py
```

The default configuration generates a training presentation on **Hybrid Cloud Security** with 10 slides.

### Command-Line Arguments

```bash
python main.py --topic "Zero Trust Architecture" \
               --subpoints "Identity,Device Trust,Network Segmentation" \
               --slides 15 \
               --model ollama/deepseek-v4-pro:cloud \
               --fallback-model ollama/glm-5.1
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--topic` | `Hybrid Cloud Security` | Topic for the training material |
| `--subpoints` | `IAM Federation,KMS...` | Comma-separated subpoints |
| `--references` | `NIST SP 800-144...` | Reference standards |
| `--slides` | `10` | Minimum number of slides |
| `--model` | `ollama/deepseek-v4-pro:cloud` | Primary LLM model |
| `--fallback-model` | `ollama/glm-5.1` | Fallback LLM on rate limit |
| `--style` | `Corporate` | Visual style name |
| `--colors` | `Blue/White` | Color palette hint |

### Model Selection

The app supports multiple LLM providers via CrewAI/LiteLLM:

| Provider | Example Model String |
|----------|---------------------|
| **Ollama (Local)** | `ollama/llama3.1`, `ollama/deepseek-r1:14b` |
| **Ollama (Cloud)** | `ollama/deepseek-v4-pro:cloud`, `ollama/glm-5.1` |
| **Gemini** | `gemini/gemini-2.5-flash`, `gemini/gemini-1.5-pro` |
| **OpenAI** | `gpt-4o`, `gpt-4-turbo` |
| **Anthropic** | `claude-3-5-sonnet-20241022` |

Set the model via:
- `--model` CLI argument
- `OLLAMA_MODEL` environment variable
- `GEMINI_API_KEY` environment variable (auto-selects Gemini)

### Fallback Behavior

If the primary model returns a `429 RESOURCE_EXHAUSTED` or rate-limit error, the app automatically retries with the `--fallback-model`.

### Ollama Setup

**Local Ollama:**

1. Install Ollama: https://ollama.com/download
2. Pull your model:
   ```bash
   ollama pull deepseek-v4-pro:cloud
   ```
3. Ensure Ollama is running:
   ```bash
   ollama serve
   ```

**Ollama Cloud:**

Set the cloud endpoint:
```bash
export OLLAMA_HOST=https://api.ollama.ai
```

### Customizing the Theme

Edit `default_seed_schema.md` to adjust colors, fonts, and layout rules. The Creative Director agent loads this file automatically.

## Customizing Visual Identity

The `default_seed_schema.md` file defines the default **Corporate Deep Blue** theme. You can:

- Change hex color codes in the palette table
- Adjust font sizes and families
- Modify slide layout rules (margins, bar heights, column widths)
- Add new theme sections (e.g., "Healthcare", "Finance")

## Agent Tools Reference

| Tool | Purpose | File |
|------|---------|------|
| `internet_search` | DuckDuckGo web search | `tools/search_tools.py` |
| `generate_infra_diagram` | Run `diagrams` Python scripts | `tools/diagram_tools.py` |
| `generate_diagram_with_fallback` | Diagrams + image fallback | `tools/diagram_tools.py` |
| `validate_diagram_script` | Syntax-check diagram code | `tools/diagram_tools.py` |
| `fetch_technical_image` | Search and download images | `tools/image_tools.py` |
| `prepare_image_for_slide` | Resize images for slides | `tools/image_tools.py` |
| `create_final_ppt` | Generate `.pptx` | `tools/file_tools.py` |
| `create_reference_doc` | Generate `.docx` | `tools/file_tools.py` |
| `load_default_schema` | Parse theme from markdown | `tools/schema_loader.py` |

## Development

### Adding a New Agent

1. Create a new file in `agents/`
2. Define a `get_<role>()` factory function returning a `crewai.Agent`
3. Register the agent and its task in `main.py`

### Adding a New Tool

1. Define the function in the appropriate `tools/*.py` file
2. Add a docstring (required by CrewAI)
3. Decorate with `@tool("tool_name")`
4. Register the tool in the relevant agent

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `No GEMINI_API_KEY found` | Create a `.env` file with your API key |
| Diagram generation fails | Ensure Graphviz is installed and on PATH |
| `diagrams` import error | Run `pip install diagrams` |
| Images not appearing | Check `temp/` directory permissions |
| PPT styling looks off | Verify `default_seed_schema.md` is present |

## Dependencies

Key packages:

- `crewai` — Agent orchestration
- `python-pptx` — PowerPoint generation
- `python-docx` — Word document generation
- `diagrams` — Infrastructure diagramming
- `pydantic` — Data validation
- `python-dotenv` — Environment variable loading
- `langchain` / `langchain-community` — LLM integrations
- `duckduckgo-search` — Web search

See `requirements.txt` for the full list.

## License

[Your License Here]

## Contributing

Please read `AGENTS.md` for repository guidelines before contributing.
