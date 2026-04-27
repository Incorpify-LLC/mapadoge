from crewai import Task
from models import ContentScript

def get_scripting_task(agent, context_tasks, min_slides=10):
    return Task(
        description=f"""Using the Master Research Document, create two distinct outputs:
        1. Slides: Generate AT LEAST {min_slides} slides. Cover every technical subpoint
           (SAML, OAuth, VPN Architecture, etc.) in granular detail across multiple slides.
           Each slide MUST have a unique diagram_prompt.
           If the slide topic is well-suited to an infrastructure diagram (e.g., network
           architecture, data flow, system topology), you MAY also provide a diagram_script
           field containing valid Python code using the diagrams library.
        2. Manual: A massive, detailed reference manual based on the 2000-word synthesis.
        Ensure every technical detail found or known is included.""",
        expected_output=f"A structured script with AT LEAST {min_slides} slides and a massive manual.",
        agent=agent,
        context=context_tasks,
        output_pydantic=ContentScript
    )
