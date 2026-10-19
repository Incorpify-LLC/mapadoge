"""Tests for tools/schema_loader.py."""

import sys
import os
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.schema_parser import parse_seed_schema

SAMPLE_SCHEMA = """\
# Default Seed Schema

## Theme: Corporate Deep Blue

### Palette

| Role         | Hex       | RGB            | Usage            |
|--------------|-----------|----------------|------------------|
| Primary      | `#0F2C59` | `15, 44, 89`   | Headers          |
| Secondary    | `#1E5F74` | `30, 95, 116`  | Sub-headers      |
| Accent       | `#E8B931` | `232, 185, 49` | Highlights       |
| Background   | `#F5F7FA` | `245, 247, 250`| Slide background |

### Typography

| Element | Font Family | Size (pt) | Weight | Color        |
|---------|-------------|-----------|--------|--------------|
| Title   | Calibri     | 36        | Bold   | Text Inverse |
"""


def test_parse_seed_schema_normalizes_roles():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(SAMPLE_SCHEMA)
        f.flush()
        result = parse_seed_schema(f.name)

    assert result["primary_color"] == "#0F2C59"
    assert result["secondary_color"] == "#1E5F74"
    assert result["accent_color"] == "#E8B931"
    assert result["background_color"] == "#F5F7FA"


def test_parse_seed_schema_defaults():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(SAMPLE_SCHEMA)
        f.flush()
        result = parse_seed_schema(f.name)

    assert result["header_font_size"] == 36
    assert result["body_font_size"] == 20
    assert result["font_family"] == "Calibri"
    assert result["theme_name"] == "Corporate Deep Blue"
