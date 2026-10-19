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
        Preserve the layout_type, subtitle, and attribution from each SlideContent
        into the corresponding FinalSlideData entry so the compiler can render the
        correct layout. Each slide should have either a diagram_path or an image_path set.""",
        expected_output="A complete VisualPackage with bullets, layout_type, and verified image paths for every slide.",
        agent=agent,
        context=context_tasks,
        output_pydantic=VisualPackage
    )
