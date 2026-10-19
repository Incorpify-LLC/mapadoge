"""Tests for configuration loading in config.py."""

import sys
import os
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import load_config, resolve


def test_load_config_missing_file():
    result = load_config("/nonexistent/path/config.yaml")
    assert result == {}


def test_load_config_valid_yaml():
    content = "topic: Test Topic\nslides: 15\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(content)
        f.flush()
        result = load_config(f.name)
    assert result["topic"] == "Test Topic"
    assert result["slides"] == 15


def test_resolve_cli_overrides_config():
    cfg = {"topic": "From Config"}
    assert resolve("From CLI", cfg, "topic", "Fallback") == "From CLI"


def test_resolve_config_overrides_fallback():
    cfg = {"topic": "From Config"}
    assert resolve(None, cfg, "topic", "Fallback") == "From Config"


def test_resolve_fallback_when_missing():
    cfg = {}
    assert resolve(None, cfg, "topic", "Fallback") == "Fallback"


def test_resolve_none_in_config():
    cfg = {"model": None}
    assert resolve(None, cfg, "model", "default-model") == "default-model"
