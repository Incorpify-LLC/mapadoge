from crewai import Agent
from tools.diagram_tools import generate_infra_diagram, generate_diagram_with_fallback, validate_diagram_script

def get_visual_architect(style, colors, llm="ollama/deepseek-v4-pro:cloud"):
    return Agent(
        role="Visual Design Architect",
        goal=f"Create infrastructure diagrams and design specs using {style} and {colors}.",
        backstory="""Master of visual hierarchy and infrastructure diagramming.
        You analyze SlideContent prompts and generate high-quality Python diagrams code
        using the diagrams library + Graphviz. You MUST provide a unique filename for every diagram.
        If a slide includes a diagram_script, validate and execute it. If diagram generation fails,
        trigger the fallback image search automatically. You produce a DesignSpecs mapping
        every slide to its visual asset.""",
        llm=llm,
        tools=[generate_infra_diagram, generate_diagram_with_fallback, validate_diagram_script],
        verbose=True
    )
