from crewai import Task
from models import StyleConfig
from tools.schema_loader import load_default_schema

def get_style_task(agent, topic):
    return Task(
        description=f"""Develop a professional visual identity for a presentation on {topic}.
        Load the default seed schema using the load_default_schema tool to get the base palette.
        Choose a primary and secondary color that matches the corporate and technical nature
        of the topic. Define optimal font sizes for headers and body text.
        Return a complete StyleConfig including theme_name, accent_color, background_color,
        text_primary, and text_inverse.""",
        expected_output="A professional style configuration (StyleConfig) aligned with the default seed schema.",
        agent=agent,
        output_pydantic=StyleConfig
    )
