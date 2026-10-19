"""Tests for pure functions in tools/file_tools.py."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.render_utils import hex_to_rgb, chunk_bullets, build_slide_entries
from pptx.dml.color import RGBColor


def test_hex_to_rgb_6_digit():
    assert hex_to_rgb("#0F2C59") == RGBColor(0x0F, 0x2C, 0x59)


def test_hex_to_rgb_3_digit():
    assert hex_to_rgb("#FFF") == RGBColor(0xFF, 0xFF, 0xFF)


def test_hex_to_rgb_no_hash():
    assert hex_to_rgb("E8B931") == RGBColor(0xE8, 0xB9, 0x31)


def test_chunk_bullets_under_limit():
    bullets = ["a", "b", "c"]
    assert chunk_bullets(bullets, max_per_slide=6) == [["a", "b", "c"]]


def test_chunk_bullets_exact_limit():
    bullets = ["a", "b", "c", "d", "e", "f"]
    assert chunk_bullets(bullets, max_per_slide=6) == [["a", "b", "c", "d", "e", "f"]]


def test_chunk_bullets_over_limit():
    bullets = ["a", "b", "c", "d", "e", "f", "g"]
    result = chunk_bullets(bullets, max_per_slide=6)
    assert result == [["a", "b", "c", "d", "e", "f"], ["g"]]


def test_chunk_bullets_empty():
    assert chunk_bullets([], max_per_slide=6) == []


def test_build_slide_entries_single():
    data = [{"title": "Slide 1", "bullets": ["a", "b"]}]
    entries = build_slide_entries(data)
    assert len(entries) == 1
    assert entries[0]["title"] == "Slide 1"
    assert entries[0]["bullets"] == ["a", "b"]


def test_build_slide_entries_split():
    data = [{"title": "Long Slide", "bullets": list(range(8))}]
    entries = build_slide_entries(data)
    assert len(entries) == 2
    assert entries[0]["title"] == "Long Slide (1/2)"
    assert entries[1]["title"] == "Long Slide (2/2)"
    assert len(entries[0]["bullets"]) == 6
    assert len(entries[1]["bullets"]) == 2


def test_build_slide_entries_image_only_first():
    data = [{"title": "Visual", "bullets": list(range(8)), "diagram_path": "/tmp/diag.png"}]
    entries = build_slide_entries(data)
    assert entries[0]["diagram_path"] == "/tmp/diag.png"
    assert entries[1]["diagram_path"] is None
