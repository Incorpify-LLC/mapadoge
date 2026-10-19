"""Checkpoint utilities for mid-pipeline failure recovery.

Pure functions — no crewai dependency. Testable in isolation.
"""

import os
import json
from typing import Optional, List, Type, Any

from tools.logging_config import get_logger

logger = get_logger("tools.checkpoint")


def save_checkpoint(step_name: str, data: Any, run_id: str,
                    base_dir: str = "output/checkpoints") -> str:
    """Serialize task output to a checkpoint JSON file.

    Args:
        step_name: Identifier for the pipeline step (e.g., "synthesis").
        data: The step's output — a Pydantic model, dict, or primitive.
        run_id: The run ID this checkpoint belongs to.
        base_dir: Root directory for all checkpoints.

    Returns:
        Absolute path to the saved checkpoint file.
    """
    dir_path = os.path.join(base_dir, run_id)
    os.makedirs(dir_path, exist_ok=True)
    path = os.path.join(dir_path, f"{step_name}.json")

    if hasattr(data, "model_dump"):
        # Pydantic v2
        payload = data.model_dump(mode="json")
    elif hasattr(data, "dict"):
        # Pydantic v1
        payload = data.dict()
    elif isinstance(data, dict):
        payload = data
    else:
        payload = data

    with open(path, "w") as f:
        json.dump(payload, f, indent=2, default=str)

    logger.info("Checkpoint saved: %s", path)
    return os.path.abspath(path)


def load_checkpoint(step_name: str, run_id: str,
                    model_class: Optional[Type] = None,
                    base_dir: str = "output/checkpoints") -> Optional[Any]:
    """Load a checkpoint and optionally deserialize into a Pydantic model.

    Args:
        step_name: Identifier for the pipeline step.
        run_id: The run ID.
        model_class: If provided, deserialize JSON into this Pydantic model.
        base_dir: Root directory for all checkpoints.

    Returns:
        The deserialized data, or None if no checkpoint exists.
    """
    path = os.path.join(base_dir, run_id, f"{step_name}.json")
    if not os.path.exists(path):
        return None

    with open(path) as f:
        raw = json.load(f)

    if model_class and hasattr(model_class, "model_validate"):
        return model_class.model_validate(raw)
    if model_class and hasattr(model_class, "parse_obj"):
        return model_class.parse_obj(raw)

    return raw


# Canonical pipeline step order. Used to sort checkpoints chronologically.
STEP_ORDER = [
    "synthesis",
    "research",
    "scripting",
    "style",
    "design",
    "assets",
    "compilation",
]


def list_checkpoints(run_id: str, base_dir: str = "output/checkpoints") -> List[str]:
    """List step names that have checkpoints for a given run_id.

    Returns step names in pipeline execution order (not alphabetical).
    Unknown step names are appended at the end in alphabetical order.
    """
    dir_path = os.path.join(base_dir, run_id)
    if not os.path.isdir(dir_path):
        return []
    found = {f[:-5] for f in os.listdir(dir_path) if f.endswith(".json")}
    ordered = [s for s in STEP_ORDER if s in found]
    extras = sorted(found - set(STEP_ORDER))
    return ordered + extras


def get_latest_checkpoint(run_id: str, base_dir: str = "output/checkpoints") -> Optional[str]:
    """Return the step name of the most recent checkpoint, or None."""
    checkpoints = list_checkpoints(run_id, base_dir)
    return checkpoints[-1] if checkpoints else None


def delete_checkpoints(run_id: str, base_dir: str = "output/checkpoints") -> int:
    """Delete all checkpoints for a run_id. Returns count of deleted files."""
    import shutil
    dir_path = os.path.join(base_dir, run_id)
    if not os.path.isdir(dir_path):
        return 0
    count = len([f for f in os.listdir(dir_path) if f.endswith(".json")])
    shutil.rmtree(dir_path)
    logger.info("Deleted %d checkpoints for run %s", count, run_id)
    return count
