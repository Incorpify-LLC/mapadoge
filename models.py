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

class SlideContent(BaseModel):
    title: str
    bullet_points: List[str]
    diagram_prompt: str = Field(..., description="A prompt for the Visual Architect to generate a diagram.")
    diagram_script: Optional[str] = Field(default=None, description="Optional Python code using the diagrams library to generate the visual.")

class ManualSection(BaseModel):
    heading: str
    prose_content: str = Field(..., description="Long-form narrative content for the reference manual.")
    implementation_guide: str = Field(..., description="Deep-dive technical instructions.")
    troubleshooting: Optional[str] = None

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

class VisualPackage(BaseModel):
    slides: List[FinalSlideData]
    style: StyleConfig
