import os
from crewai.tools import tool

from tools.logging_config import get_logger
from tools.render_utils import (
    dispatch_slide_layout,
    apply_reference_doc_style,
    build_slide_entries,
)

logger = get_logger("tools.file")


@tool("create_final_ppt")
def create_final_ppt(slides_data: list, style_config: dict, run_id: str = None):
    """Generates a professional .pptx with themed styling, accent bars, and image support."""
    from pptx import Presentation
    from pptx.util import Inches

    os.makedirs("output", exist_ok=True)
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    slide_entries = build_slide_entries(slides_data)

    for i, entry in enumerate(slide_entries, start=1):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        dispatch_slide_layout(
            slide,
            entry,
            style_config,
            slide_number=i,
        )

    filename = f"training_presentation_{run_id}.pptx" if run_id else "training_presentation.pptx"
    path = os.path.join("output", filename)
    prs.save(path)
    logger.info("PPT saved: %s", path)
    return path


@tool("create_reference_doc")
def create_reference_doc(sections: list, style_config: dict, run_id: str = None):
    """Generates a detailed technical .docx manual with themed headings."""
    from docx import Document

    os.makedirs("output", exist_ok=True)
    doc = Document()

    apply_reference_doc_style(doc, sections, style_config)

    filename = f"reference_manual_{run_id}.docx" if run_id else "reference_manual.docx"
    path = os.path.join("output", filename)
    doc.save(path)
    logger.info("DOC saved: %s", path)
    return path
