from crewai import Task
from models import VisualPackage

def get_asset_coordination_task(agent, context_tasks):
    return Task(
        description="""Review the SlideContent and DesignSpecs.
        For every slide, ensure there is a valid visual asset.
        If a diagram_path from DesignSpecs is missing or the file does not exist,
        use fetch_technical_image to get a relevant technical image.
        If an image is fetched, use prepare_image_for_slide to resize it.
        Consolidate everything into a VisualPackage.
        Each slide should have either a diagram_path or an image_path set.""",
        expected_output="A complete VisualPackage with bullets and verified image paths.",
        agent=agent,
        context=context_tasks,
        output_pydantic=VisualPackage
    )
