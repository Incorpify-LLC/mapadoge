"""Configuration loading for the training material generator."""

import os

from tools.logging_config import get_logger

logger = get_logger("config")


def load_config(config_path="config.yaml"):
    """Load default values from a YAML config file if it exists."""
    try:
        import yaml
        with open(config_path) as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}
    except Exception as e:
        logger.warning("Could not load config from %s: %s", config_path, e)
        return {}


def resolve(value, config, key, fallback=None):
    """Resolve a single argument value: explicit value > config > hardcoded fallback."""
    if value is not None:
        return value
    if key in config and config[key] is not None:
        return config[key]
    return fallback
