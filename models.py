from pydantic import BaseModel, Field
from typing import List, Optional

class ResearchFact(BaseModel):
    title: str = Field(..., description="The title of the technical fact.")
    fact: str = Field(..., description="A detailed explanation of the fact.")
    technical_depth: str = Field(..., description="Additional technical context or theory.")
    implementation_steps: List[str] = Field(..., description="Steps to implement this feature or concept.")

class ResearchKB(BaseModel):
    topic: str
    facts: List[ResearchFact]
    summary: str

class BulletPoint(BaseModel):
    text: str
    level: int = Field(default=0, ge=0, le=3, description="Indentation level (0 = top, up to 3 nested levels).")


class SlideContent(BaseModel):
    title: str
    bullet_points: List[BulletPoint] = Field(default_factory=list)
    diagram_prompt: str = Field(..., description="A prompt for the Visual Architect to generate a diagram.")
    diagram_script: Optional[str] = Field(default=None, description="Optional Python code using the diagrams library to generate the visual.")
    layout_type: str = Field(default="Title and Content", description="Layout template: Title, Agenda, Title and Content, Diagram Full, Quote, Comparison, Divider.")
    subtitle: Optional[str] = Field(default=None, description="Subtitle for Title and Agenda slides.")
    attribution: Optional[str] = Field(default=None, description="Attribution for Quote slides.")

class SectionHeading(BaseModel):
    title: str
    level: int = Field(default=2, ge=1, le=3, description="Heading level (1-3).")


class ManualSection(BaseModel):
    heading: str
    prose_content: str = Field(..., description="Long-form narrative content for the reference manual.")
    implementation_guide: str = Field(..., description="Deep-dive technical instructions.")
    troubleshooting: Optional[str] = None
    custom_subheadings: Optional[List[SectionHeading]] = Field(default=None, description="Optional custom subheadings for this section.")

class ContentScript(BaseModel):
    slides: List[SlideContent]
    manual_sections: List[ManualSection]

class SlideDesignSpec(BaseModel):
    slide_title: str
    diagram_path: Optional[str] = Field(default=None, description="Absolute or relative path to a generated diagram PNG.")
    image_path: Optional[str] = Field(default=None, description="Absolute or relative path to a fetched fallback image.")
    layout_type: str = Field(default="Title and Content", description="The PPT layout to use.")

class StyleConfig(BaseModel):
    theme_name: str = Field(default="Corporate Deep Blue", description="Name of the active theme.")
    primary_color: str = Field(..., description="Hex code for primary brand color (e.g., #003366).")
    secondary_color: str = Field(..., description="Hex code for secondary/accent color.")
    accent_color: str = Field(default="#E8B931", description="Hex code for highlight/CTA color.")
    background_color: str = Field(default="#F5F7FA", description="Hex code for slide background.")
    text_primary: str = Field(default="#1A1A2E", description="Hex code for body text.")
    text_inverse: str = Field(default="#FFFFFF", description="Hex code for text on dark backgrounds.")
    header_font_size: int = Field(default=36)
    body_font_size: int = Field(default=20)
    font_family: str = Field(default="Calibri")

class DesignSpecs(BaseModel):
    specs: List[SlideDesignSpec]
    style: Optional[StyleConfig] = None

class FinalSlideData(BaseModel):
    title: str
    bullets: List[str]
    diagram_path: Optional[str] = None
    image_path: Optional[str] = None
    layout_type: str = Field(default="Title and Content", description="The PPT layout to use.")
    subtitle: Optional[str] = None
    attribution: Optional[str] = None

class VisualPackage(BaseModel):
    slides: List[FinalSlideData]
    style: StyleConfig
