"""Tests for diagram tool helpers in tools/diagram_tools.py."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.diagram_utils import inject_theme_colors


def testinject_theme_colors_with_dict():
    style = {
        "primary_color": "#003366",
        "secondary_color": "#0066CC",
        "accent_color": "#FF9900",
        "background_color": "#FFFFFF",
        "text_primary": "#000000",
        "text_inverse": "#EEEEEE",
    }
    script = "from diagrams import Diagram\nwith Diagram('Test'):\n    pass"
    result = inject_theme_colors(script, style)
    assert 'PRIMARY = "#003366"' in result
    assert 'SECONDARY = "#0066CC"' in result
    assert 'ACCENT = "#FF9900"' in result
    assert 'BACKGROUND = "#FFFFFF"' in result
    assert 'TEXT_PRIMARY = "#000000"' in result
    assert 'TEXT_INVERSE = "#EEEEEE"' in result
    assert result.endswith(script)


def testinject_theme_colors_none_config():
    script = "print('hello')"
    result = inject_theme_colors(script, None)
    assert result == script


def testinject_theme_colors_empty_config():
    script = "print('hello')"
    result = inject_theme_colors(script, {})
    assert result == script


def testinject_theme_colors_with_style_config_object():
    from models import StyleConfig
    style = StyleConfig(
        primary_color="#111111",
        secondary_color="#222222",
        accent_color="#333333",
        background_color="#444444",
        text_primary="#555555",
        text_inverse="#666666",
    )
    script = "x = 1"
    result = inject_theme_colors(script, style)
    assert 'PRIMARY = "#111111"' in result
    assert 'SECONDARY = "#222222"' in result


def testinject_theme_colors_defaults():
    """When partial config is given, missing keys use defaults."""
    style = {"primary_color": "#ABCDEF"}
    script = "pass"
    result = inject_theme_colors(script, style)
    assert 'PRIMARY = "#ABCDEF"' in result
    assert 'SECONDARY = "#1E5F74"' in result  # default
    assert 'ACCENT = "#E8B931"' in result     # default
