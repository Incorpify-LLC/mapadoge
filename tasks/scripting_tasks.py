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
           Assign a layout_type to each slide based on its content:
           - "Title" for the very first slide (include subtitle field).
           - "Agenda" for the second slide listing all subsequent slide titles.
           - "Diagram Full" for slides where the diagram is the primary content.
           - "Quote" for slides that present a key insight or callout (include attribution).
           - "Comparison" for slides that contrast two approaches or technologies.
           - "Divider" for section divider slides between logical groups.
           - "Title and Content" for all other standard slides.
           Use multi-level bullets where appropriate: set bullet level (0-3) to create
           hierarchical information structure.
        2. Manual: A massive, detailed reference manual based on the 2000-word synthesis.
           Optionally provide custom_subheadings for sections that need specialized structure.
        Ensure every technical detail found or known is included.""",
        expected_output=f"A structured script with AT LEAST {min_slides} slides and a massive manual.",
        agent=agent,
        context=context_tasks,
        output_pydantic=ContentScript
    )
