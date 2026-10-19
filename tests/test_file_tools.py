"""Tests for pure functions in tools/file_tools.py."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.render_utils import (
    hex_to_rgb,
    hex_to_doc_rgb,
    chunk_bullets,
    build_slide_entries,
    resolve_image_path,
    dispatch_slide_layout,
    generate_preview_html,
    render_title_slide,
    render_agenda_slide,
    render_diagram_full_slide,
    render_quote_slide,
    render_comparison_slide,
    render_divider_slide,
)
from pptx.dml.color import RGBColor
from pptx import Presentation
from pptx.util import Inches
from docx import Document
from docx.shared import RGBColor as DocRGBColor


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


def test_build_slide_entries_empty_bullets():
    """Layouts like Title, Divider, Diagram Full may have no bullets — they must still produce an entry."""
    data = [
        {"title": "Welcome", "bullets": [], "layout_type": "Title", "subtitle": "Sub"},
        {"title": "Part 2", "bullets": [], "layout_type": "Divider"},
        {"title": "Network", "bullets": [], "layout_type": "Diagram Full"},
    ]
    entries = build_slide_entries(data)
    assert len(entries) == 3
    assert entries[0]["title"] == "Welcome"
    assert entries[0]["layout_type"] == "Title"
    assert entries[0]["subtitle"] == "Sub"
    assert entries[1]["title"] == "Part 2"
    assert entries[1]["layout_type"] == "Divider"
    assert entries[2]["title"] == "Network"
    assert entries[2]["layout_type"] == "Diagram Full"


def test_build_slide_entries_preserves_layout_type():
    data = [{"title": "Intro", "bullets": ["a"], "layout_type": "Title", "subtitle": "Sub"}]
    entries = build_slide_entries(data)
    assert entries[0]["layout_type"] == "Title"
    assert entries[0]["subtitle"] == "Sub"


def test_build_slide_entries_layout_only_first_chunk():
    data = [{"title": "Split", "bullets": list(range(8)), "layout_type": "Comparison", "attribution": "Source"}]
    entries = build_slide_entries(data)
    assert entries[0]["layout_type"] == "Comparison"
    assert entries[0]["attribution"] == "Source"
    assert entries[1]["layout_type"] == "Comparison"
    assert entries[1]["attribution"] is None


# --- Layout rendering tests ---

def _make_style():
    return {
        "primary_color": "#0F2C59",
        "secondary_color": "#1E5F74",
        "accent_color": "#E8B931",
        "background_color": "#F5F7FA",
        "text_primary": "#1A1A2E",
        "text_inverse": "#FFFFFF",
        "font_family": "Calibri",
        "header_font_size": 36,
        "body_font_size": 20,
    }


def _new_prs():
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    return prs


def test_render_title_slide_no_error():
    prs = _new_prs()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    render_title_slide(slide, "My Title", _make_style(), subtitle="A subtitle")
    assert slide is not None


def test_render_agenda_slide_no_error():
    prs = _new_prs()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    render_agenda_slide(slide, "Agenda", ["Topic A", "Topic B", "Topic C"], _make_style())
    assert slide is not None


def test_render_diagram_full_slide_no_error():
    prs = _new_prs()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    render_diagram_full_slide(slide, "Architecture", _make_style(), caption="Fig 1: Overview")
    assert slide is not None


def test_render_quote_slide_no_error():
    prs = _new_prs()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    render_quote_slide(slide, "Key Insight", _make_style(), quote_text="Security is a process, not a product.", attribution="Bruce Schneier")
    assert slide is not None


def test_render_comparison_slide_no_error():
    prs = _new_prs()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    render_comparison_slide(slide, "SAML vs OAuth", ["SAML is XML-based", "Enterprise SSO", "OAuth is JSON-based", "Modern API auth"], _make_style())
    assert slide is not None


def test_render_divider_slide_no_error():
    prs = _new_prs()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    render_divider_slide(slide, "Section 2: Advanced Topics", _make_style())
    assert slide is not None


def test_dispatch_title_layout():
    prs = _new_prs()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    entry = {"layout_type": "Title", "title": "Welcome", "bullets": [], "subtitle": "Training Day 1"}
    dispatch_slide_layout(slide, entry, _make_style(), slide_number=1)
    assert slide is not None


def test_dispatch_agenda_layout():
    prs = _new_prs()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    entry = {"layout_type": "Agenda", "title": "Agenda", "bullets": ["Intro", "Deep Dive"]}
    dispatch_slide_layout(slide, entry, _make_style(), slide_number=2)
    assert slide is not None


def test_dispatch_diagram_full_layout():
    prs = _new_prs()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    entry = {"layout_type": "Diagram Full", "title": "Network", "bullets": []}
    dispatch_slide_layout(slide, entry, _make_style(), slide_number=3)
    assert slide is not None


def test_dispatch_quote_layout():
    prs = _new_prs()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    entry = {"layout_type": "Quote", "title": "Insight", "bullets": [{"text": "Zero trust never sleeps."}], "attribution": "NIST"}
    dispatch_slide_layout(slide, entry, _make_style(), slide_number=4)
    assert slide is not None


def test_dispatch_comparison_layout():
    prs = _new_prs()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    entry = {"layout_type": "Comparison", "title": "Old vs New", "bullets": ["Legacy", "Modern"]}
    dispatch_slide_layout(slide, entry, _make_style(), slide_number=5)
    assert slide is not None


def test_dispatch_divider_layout():
    prs = _new_prs()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    entry = {"layout_type": "Divider", "title": "Part 2", "bullets": []}
    dispatch_slide_layout(slide, entry, _make_style(), slide_number=6)
    assert slide is not None


def test_dispatch_default_content_layout():
    prs = _new_prs()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    entry = {"title": "Standard", "bullets": ["point A", "point B"]}
    dispatch_slide_layout(slide, entry, _make_style(), slide_number=7)
    assert slide is not None


# --- DOCX helper tests ---

def test_hex_to_doc_rgb():
    assert hex_to_doc_rgb("#0F2C59") == DocRGBColor(0x0F, 0x2C, 0x59)


def test_resolve_image_path_missing():
    assert resolve_image_path("/nonexistent/a.png", "/nonexistent/b.png") is None


def test_resolve_image_path_priority_diagram():
    # diagram_path is checked first
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        f.write(b"x")
        path = f.name
    result = resolve_image_path(path, "/nonexistent/b.png")
    assert result == os.path.abspath(path)
    os.unlink(path)


# --- DOCX conditional subheadings test ---

def test_apply_reference_doc_style_conditional_headings():
    from tools.render_utils import apply_reference_doc_style
    doc = Document()
    sections = [
        {
            "heading": "Section A",
            "prose_content": "Some prose.",
            "implementation_guide": "How to implement.",
            "troubleshooting": "Watch out for X.",
        },
        {
            "heading": "Section B",
            "prose_content": "More prose.",
            "implementation_guide": "More implementation.",
            "troubleshooting": None,
        },
    ]
    style = {
        "primary_color": "#0F2C59",
        "secondary_color": "#1E5F74",
        "text_primary": "#1A1A2E",
    }
    apply_reference_doc_style(doc, sections, style)
    headings = [p.text for p in doc.paragraphs if p.style.name.startswith("Heading")]
    assert "Section A" in headings
    assert "Section B" in headings
    assert "Troubleshooting & Security Considerations" in headings
    # Section B has no troubleshooting, so only one Troubleshooting heading
    assert headings.count("Troubleshooting & Security Considerations") == 1


def test_generate_preview_html():
    import tempfile
    import shutil
    tmpdir = tempfile.mkdtemp()
    try:
        entries = [
            {"title": "Intro", "layout_type": "Title"},
            {"title": "Agenda", "layout_type": "Agenda"},
            {"title": "Deep Dive", "layout_type": "Title and Content"},
        ]
        path = generate_preview_html("test_run", entries, output_dir=tmpdir)
        assert os.path.exists(path)
        with open(path) as f:
            html = f.read()
        assert "Intro" in html
        assert "Agenda" in html
        assert "Deep Dive" in html
        assert "3 slides" in html
        assert "test_run" in html
    finally:
        shutil.rmtree(tmpdir)


def test_apply_reference_doc_style_custom_subheadings():
    from tools.render_utils import apply_reference_doc_style
    doc = Document()
    sections = [
        {
            "heading": "Custom Section",
            "prose_content": "Prose here.",
            "implementation_guide": "Implementation here.",
            "custom_subheadings": [
                {"title": "Architecture Overview", "level": 2},
                {"title": "Deployment Steps", "level": 3},
            ],
        },
    ]
    style = {
        "primary_color": "#0F2C59",
        "secondary_color": "#1E5F74",
        "text_primary": "#1A1A2E",
    }
    apply_reference_doc_style(doc, sections, style)
    headings = [p.text for p in doc.paragraphs if p.style.name.startswith("Heading")]
    assert "Architecture Overview" in headings
    assert "Deployment Steps" in headings
