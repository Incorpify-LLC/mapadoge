from crewai import Agent
from tools.image_tools import fetch_technical_image, prepare_image_for_slide
from tools.diagram_tools import generate_infra_diagram

def get_visual_asset_manager(llm="ollama/deepseek-v4-pro:cloud"):
    return Agent(
        role="Visual Asset Coordinator",
        goal="Ensure every slide has a valid visual asset (diagram or image).",
        backstory="""You are a creative asset manager. Review DesignSpecs and SlideContent.
        If a diagram_path is missing, invalid, or the file does not exist, you MUST fetch a
        relevant technical image using your tool. If an image is fetched, prepare it for the slide.
        At least 50% of slides should have diagrams; the rest can use curated web images.
        You produce the final VisualPackage for the Compiler.""",
        llm=llm,
        tools=[fetch_technical_image, prepare_image_for_slide, generate_infra_diagram],
        verbose=True
    )
