import os
import sys
import argparse
from dotenv import load_dotenv
load_dotenv()

from crewai import Crew, Process

from agents.librarian import get_librarian
from agents.researcher import get_researcher
from agents.scriptwriter import get_scriptwriter
from agents.creative_director import get_creative_director
from agents.visual_architect import get_visual_architect
from agents.visual_asset_manager import get_visual_asset_manager
from agents.compiler import get_compiler

from tasks.librarian_tasks import get_synthesis_task
from tasks.research_tasks import get_research_task
from tasks.scripting_tasks import get_scripting_task
from tasks.style_tasks import get_style_task
from tasks.design_tasks import get_design_task
from tasks.visual_tasks import get_asset_coordination_task
from tasks.compilation_tasks import get_compilation_task

from tools.schema_loader import parse_seed_schema

_DEFAULT_MODEL = "ollama/deepseek-v4-pro:cloud"
_FALLBACK_MODEL = "ollama/glm-5.1"

def _resolve_llm(model=None):
    """Resolve LLM string with fallback logic."""
    if model:
        return model
    if os.getenv("OLLAMA_MODEL"):
        return os.getenv("OLLAMA_MODEL")
    if os.getenv("GEMINI_API_KEY"):
        return "gemini/gemini-2.5-flash"
    return _DEFAULT_MODEL

def _try_model_with_fallback(llm_str):
    """Try primary model; if it looks like a local Ollama model and fails, try fallback."""
    # CrewAI handles model selection internally; we just pass the string.
    # If the user explicitly provided a model, use it.
    # Otherwise fall back to glm-5.1 if deepseek is unavailable.
    return llm_str

class TrainingAppOrchestrator:
    def __init__(self, topic, subpoints, references, style="Corporate", colors="Blue/White",
                 min_slides=10, model=None):
        llm = _try_model_with_fallback(_resolve_llm(model))
        print(f"Using LLM: {llm}")

        self.librarian = get_librarian(llm=llm)
        self.researcher = get_researcher(topic, references, llm=llm)
        self.scriptwriter = get_scriptwriter(llm=llm)
        self.creative_director = get_creative_director(llm=llm)
        self.architect = get_visual_architect(style, colors, llm=llm)
        self.visual_asset_manager = get_visual_asset_manager(llm=llm)
        self.compiler = get_compiler(llm=llm)

        self.t1 = get_synthesis_task(self.librarian, topic)
        self.t2 = get_research_task(self.researcher, topic, subpoints)
        self.t3 = get_scripting_task(self.scriptwriter, [self.t1, self.t2], min_slides=min_slides)
        self.t4 = get_style_task(self.creative_director, topic)
        self.t5 = get_design_task(self.architect, [self.t3])
        self.t6 = get_asset_coordination_task(self.visual_asset_manager, [self.t3, self.t5, self.t4])
        self.t7 = get_compilation_task(self.compiler, [self.t3, self.t6])

    def run(self):
        crew = Crew(
            agents=[
                self.librarian,
                self.researcher,
                self.scriptwriter,
                self.creative_director,
                self.architect,
                self.visual_asset_manager,
                self.compiler,
            ],
            tasks=[self.t1, self.t2, self.t3, self.t4, self.t5, self.t6, self.t7],
            process=Process.sequential,
        )
        return crew.kickoff()

def main():
    parser = argparse.ArgumentParser(
        description="AI Training Material Generator - Multi-agent PPT & Doc creator"
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="Hybrid Cloud Security",
        help="Topic for the training material (default: Hybrid Cloud Security)"
    )
    parser.add_argument(
        "--subpoints",
        type=str,
        default="IAM Federation,KMS and Encryption,IPsec VPN Architecture",
        help="Comma-separated list of subpoints (default: IAM Federation,KMS and Encryption,IPsec VPN Architecture)"
    )
    parser.add_argument(
        "--references",
        type=str,
        default="NIST SP 800-144, 800-145, 800-204",
        help="Reference standards or sources"
    )
    parser.add_argument(
        "--slides",
        type=int,
        default=10,
        help="Minimum number of slides to generate (default: 10)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="LLM model string (e.g., ollama/deepseek-v4-pro:cloud, ollama/glm-5.1, gemini/gemini-2.5-flash)"
    )
    parser.add_argument(
        "--fallback-model",
        type=str,
        default="ollama/glm-5.1",
        help="Fallback LLM model if primary fails (default: ollama/glm-5.1)"
    )
    parser.add_argument(
        "--style",
        type=str,
        default="Corporate",
        help="Visual style name (default: Corporate)"
    )
    parser.add_argument(
        "--colors",
        type=str,
        default="Blue/White",
        help="Color palette hint (default: Blue/White)"
    )
    args = parser.parse_args()

    subpoints = [s.strip() for s in args.subpoints.split(",") if s.strip()]

    schema = parse_seed_schema()
    print("Loaded theme:", schema.get("theme_name", "default"))

    app = TrainingAppOrchestrator(
        topic=args.topic,
        subpoints=subpoints,
        references=args.references,
        style=args.style,
        colors=args.colors,
        min_slides=args.slides,
        model=args.model,
    )
    try:
        result = app.run()
        print("\n=== Execution Complete ===")
        print(result)
    except Exception as e:
        err_msg = str(e).lower()
        if "429" in err_msg or "resource_exhausted" in err_msg or "rate" in err_msg:
            print(f"\nPrimary model failed with rate limit / exhaustion: {e}")
            if args.fallback_model and args.fallback_model != args.model:
                print(f"Trying fallback model: {args.fallback_model}")
                app = TrainingAppOrchestrator(
                    topic=args.topic,
                    subpoints=subpoints,
                    references=args.references,
                    style=args.style,
                    colors=args.colors,
                    min_slides=args.slides,
                    model=args.fallback_model,
                )
                result = app.run()
                print("\n=== Execution Complete (Fallback) ===")
                print(result)
            else:
                raise
        else:
            raise

if __name__ == "__main__":
    main()
