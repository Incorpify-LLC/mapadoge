"""Tests for checkpoint utilities in tools/checkpoint.py."""

import sys
import os
import tempfile
import shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.checkpoint import (
    save_checkpoint,
    load_checkpoint,
    list_checkpoints,
    get_latest_checkpoint,
    delete_checkpoints,
)
from pydantic import BaseModel


class FakeModel(BaseModel):
    name: str
    value: int


def _temp_base():
    return tempfile.mkdtemp(prefix="ckpt_test_")


def test_save_and_load_pydantic():
    base = _temp_base()
    try:
        model = FakeModel(name="test", value=42)
        path = save_checkpoint("step1", model, "run001", base_dir=base)
        assert os.path.exists(path)
        loaded = load_checkpoint("step1", "run001", model_class=FakeModel, base_dir=base)
        assert loaded.name == "test"
        assert loaded.value == 42
    finally:
        shutil.rmtree(base)


def test_save_and_load_dict():
    base = _temp_base()
    try:
        data = {"key": "value", "nested": {"a": 1}}
        save_checkpoint("step2", data, "run002", base_dir=base)
        loaded = load_checkpoint("step2", "run002", base_dir=base)
        assert loaded == data
    finally:
        shutil.rmtree(base)


def test_load_missing_checkpoint():
    base = _temp_base()
    try:
        result = load_checkpoint("nonexistent", "run999", base_dir=base)
        assert result is None
    finally:
        shutil.rmtree(base)


def test_list_checkpoints_empty():
    base = _temp_base()
    try:
        result = list_checkpoints("run_empty", base_dir=base)
        assert result == []
    finally:
        shutil.rmtree(base)


def test_list_checkpoints_multiple():
    base = _temp_base()
    try:
        save_checkpoint("alpha", {"x": 1}, "run003", base_dir=base)
        save_checkpoint("beta", {"y": 2}, "run003", base_dir=base)
        save_checkpoint("gamma", {"z": 3}, "run003", base_dir=base)
        result = list_checkpoints("run003", base_dir=base)
        assert result == ["alpha", "beta", "gamma"]
    finally:
        shutil.rmtree(base)


def test_get_latest_checkpoint():
    base = _temp_base()
    try:
        assert get_latest_checkpoint("run_none", base_dir=base) is None
        save_checkpoint("synthesis", {"done": True}, "run004", base_dir=base)
        save_checkpoint("research", {"done": True}, "run004", base_dir=base)
        assert get_latest_checkpoint("run004", base_dir=base) == "research"
    finally:
        shutil.rmtree(base)


def test_delete_checkpoints():
    base = _temp_base()
    try:
        save_checkpoint("a", {"x": 1}, "run005", base_dir=base)
        save_checkpoint("b", {"y": 2}, "run005", base_dir=base)
        count = delete_checkpoints("run005", base_dir=base)
        assert count == 2
        assert list_checkpoints("run005", base_dir=base) == []
    finally:
        shutil.rmtree(base)


def test_delete_nonexistent():
    base = _temp_base()
    try:
        count = delete_checkpoints("no_such_run", base_dir=base)
        assert count == 0
    finally:
        shutil.rmtree(base)


def test_checkpoint_isolation_between_runs():
    base = _temp_base()
    try:
        save_checkpoint("step1", {"run": "A"}, "runA", base_dir=base)
        save_checkpoint("step1", {"run": "B"}, "runB", base_dir=base)
        loaded_a = load_checkpoint("step1", "runA", base_dir=base)
        loaded_b = load_checkpoint("step1", "runB", base_dir=base)
        assert loaded_a["run"] == "A"
        assert loaded_b["run"] == "B"
    finally:
        shutil.rmtree(base)
