from crewai import Task
from models import DesignSpecs

def get_design_task(agent, context_tasks):
    return Task(
        description="""Generate a unique infrastructure diagram for EVERY SINGLE slide.
        You MUST provide a unique filename for each diagram to avoid overwriting.
        For each SlideContent, analyze the diagram_prompt and write Python code using the diagrams library.
        If the SlideContent already contains a diagram_script, validate it and execute it.
        If a diagram script fails to produce a PNG, note the failure so the Visual Asset Manager can fall back to an image.
        Return a structured DesignSpecs with a unique diagram_path for every slide.""",
        expected_output="A structured mapping of unique diagrams to every slide.",
        agent=agent,
        context=context_tasks,
        output_pydantic=DesignSpecs
    )
