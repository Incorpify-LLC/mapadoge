import os
import sys
import json
import argparse
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

from tools.logging_config import setup_logging, get_logger
from config import load_config, resolve

setup_logging(os.getenv("LOG_LEVEL", "INFO"))
logger = get_logger("orchestrator")

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

from tools.schema_parser import parse_seed_schema
from tools.checkpoint import (
    save_checkpoint,
    load_checkpoint,
    list_checkpoints,
    get_latest_checkpoint,
    STEP_ORDER,
)

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
                 min_slides=10, model=None, run_id=None):
        llm = _try_model_with_fallback(_resolve_llm(model))
        logger.info("Using LLM: %s", llm)

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
        self.t7 = get_compilation_task(self.compiler, [self.t3, self.t6], run_id=run_id)

    def _attach_checkpoint_callbacks(self, run_id):
        """Attach post-task callbacks that save checkpoints after each task completes."""
        step_map = {
            "synthesis": self.t1,
            "research": self.t2,
            "scripting": self.t3,
            "style": self.t4,
            "design": self.t5,
            "assets": self.t6,
            "compilation": self.t7,
        }
        for step_name, task in step_map.items():
            task.callback = self._make_checkpoint_callback(step_name, run_id)

    def _make_checkpoint_callback(self, step_name, run_id):
        """Create a callback that saves the task output as a checkpoint."""
        def _callback(task_output):
            try:
                save_checkpoint(step_name, task_output.raw, run_id)
                logger.info("Checkpoint saved for step '%s'", step_name)
            except Exception as e:
                logger.warning("Failed to save checkpoint for '%s': %s", step_name, e)
            return task_output
        return _callback

    def run(self, run_id=None, resume=False):
        """Execute the agent pipeline, optionally resuming from checkpoints.

        Args:
            run_id: Timestamp-based run identifier for checkpointing.
            resume: If True, skip steps that already have valid checkpoints.
        """
        if resume and run_id:
            completed = list_checkpoints(run_id)
            latest = get_latest_checkpoint(run_id)
            logger.info("Resuming run '%s'. Completed steps: %s (latest: %s)",
                        run_id, completed, latest)
            tasks_to_run = self._filter_completed_tasks(completed)
            if not tasks_to_run:
                logger.info("All steps already have checkpoints. Nothing to resume.")
                return None
        else:
            tasks_to_run = [self.t1, self.t2, self.t3, self.t4, self.t5, self.t6, self.t7]
            if run_id:
                self._attach_checkpoint_callbacks(run_id)

        agents = self._agents_for_tasks(tasks_to_run)

        crew = Crew(
            agents=agents,
            tasks=tasks_to_run,
            process=Process.sequential,
        )
        result = crew.kickoff()
        self.usage_metrics = getattr(crew, "usage_metrics", None)
        if self.usage_metrics:
            logger.info("Token usage — total: %s, prompt: %s, completion: %s",
                        self.usage_metrics.get("total_tokens", "?"),
                        self.usage_metrics.get("prompt_tokens", "?"),
                        self.usage_metrics.get("completion_tokens", "?"))
        return result

    def _filter_completed_tasks(self, completed_steps):
        """Return only tasks whose step names are NOT in completed_steps."""
        step_to_task = {
            "synthesis": self.t1,
            "research": self.t2,
            "scripting": self.t3,
            "style": self.t4,
            "design": self.t5,
            "assets": self.t6,
            "compilation": self.t7,
        }
        return [task for step, task in step_to_task.items() if step not in completed_steps]

    def _agents_for_tasks(self, tasks):
        """Return the set of agents needed for the given tasks."""
        agent_map = {
            id(self.t1): self.librarian,
            id(self.t2): self.researcher,
            id(self.t3): self.scriptwriter,
            id(self.t4): self.creative_director,
            id(self.t5): self.architect,
            id(self.t6): self.visual_asset_manager,
            id(self.t7): self.compiler,
        }
        seen = set()
        agents = []
        for task in tasks:
            for task_id, agent in agent_map.items():
                if task_id == id(task) and id(agent) not in seen:
                    agents.append(agent)
                    seen.add(id(agent))
                    break
        return agents

def write_run_metadata(run_id, topic, model, style, schema_name, usage_metrics=None, fallback=False):
    """Write a run_metadata_{run_id}.json sidecar with execution details."""
    os.makedirs("output", exist_ok=True)
    metadata = {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "model": model,
        "style": style,
        "theme": schema_name,
        "fallback_used": fallback,
    }
    if usage_metrics:
        metadata["usage_metrics"] = usage_metrics
    path = os.path.join("output", f"run_metadata_{run_id}.json")
    with open(path, "w") as f:
        json.dump(metadata, f, indent=2, default=str)
    logger.info("Run metadata saved: %s", path)
    return path


def main():
    config = load_config()
    logger.info("Config loaded: %s", config if config else "none (using defaults)")

    parser = argparse.ArgumentParser(
        description="AI Training Material Generator - Multi-agent PPT & Doc creator"
    )
    parser.add_argument("--topic", type=str, default=None, help="Topic for the training material")
    parser.add_argument("--subpoints", type=str, default=None, help="Comma-separated subpoints")
    parser.add_argument("--references", type=str, default=None, help="Reference standards or sources")
    parser.add_argument("--slides", type=int, default=None, help="Minimum number of slides")
    parser.add_argument("--model", type=str, default=None, help="LLM model string")
    parser.add_argument("--fallback-model", type=str, default=None, help="Fallback LLM model")
    parser.add_argument("--style", type=str, default=None, help="Visual style name")
    parser.add_argument("--colors", type=str, default=None, help="Color palette hint")
    parser.add_argument("--resume", type=str, default=None,
                        help="Resume a previous run by its run_id (skips completed steps)")
    args = parser.parse_args()

    topic = resolve(args.topic, config, "topic", "Hybrid Cloud Security")
    subpoints_raw = resolve(args.subpoints, config, "subpoints", "IAM Federation,KMS and Encryption,IPsec VPN Architecture")
    references = resolve(args.references, config, "references", "NIST SP 800-144, 800-145, 800-204")
    slides = resolve(args.slides, config, "slides", 10)
    fallback_model = resolve(args.fallback_model, config, "fallback_model", "ollama/glm-5.1")
    style = resolve(args.style, config, "style", "Corporate")
    colors = resolve(args.colors, config, "colors", "Blue/White")

    subpoints = subpoints_raw if isinstance(subpoints_raw, list) else [s.strip() for s in subpoints_raw.split(",") if s.strip()]

    schema = parse_seed_schema()
    logger.info("Loaded theme: %s", schema.get("theme_name", "default"))

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger.info("Run ID: %s", run_id)

    model = resolve(args.model, config, "model")

    resume = args.resume is not None
    active_run_id = args.resume if resume else run_id
    if resume:
        completed = list_checkpoints(active_run_id)
        logger.info("Resuming run '%s'. Already completed: %s", active_run_id, completed)

    app = TrainingAppOrchestrator(
        topic=topic,
        subpoints=subpoints,
        references=references,
        style=style,
        colors=colors,
        min_slides=slides,
        model=model,
        run_id=active_run_id,
    )
    try:
        result = app.run(run_id=active_run_id, resume=resume)
        logger.info("Execution complete")
        write_run_metadata(active_run_id, topic, model, style, schema.get("theme_name", "default"), usage_metrics=app.usage_metrics)
        print("\n=== Execution Complete ===")
        print(result)
    except Exception as e:
        err_msg = str(e).lower()
        if "429" in err_msg or "resource_exhausted" in err_msg or "rate" in err_msg:
            logger.warning("Primary model rate limited: %s", e)
            if fallback_model and fallback_model != model:
                logger.info("Trying fallback model: %s", fallback_model)
                app = TrainingAppOrchestrator(
                    topic=topic,
                    subpoints=subpoints,
                    references=references,
                    style=style,
                    colors=colors,
                    min_slides=slides,
                    model=fallback_model,
                    run_id=active_run_id,
                )
                result = app.run(run_id=active_run_id, resume=resume)
                write_run_metadata(active_run_id, topic, fallback_model, style, schema.get("theme_name", "default"), usage_metrics=app.usage_metrics, fallback=True)
                print("\n=== Execution Complete (Fallback) ===")
                print(result)
            else:
                raise
        else:
            raise

if __name__ == "__main__":
    main()
