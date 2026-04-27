from crewai import Task
from models import ResearchKB

def get_research_task(agent, topic, subpoints):
    return Task(
        description=f"""Analyze {topic} and the subpoints: {subpoints}. 
        Provide a technical deep dive with implementation steps and troubleshooting tips.""",
        expected_output="A structured technical knowledge base.",
        agent=agent,
        output_pydantic=ResearchKB
    )
