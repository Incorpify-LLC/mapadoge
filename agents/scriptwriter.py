from crewai import Agent

def get_scriptwriter(llm="ollama/deepseek-v4-pro:cloud"):
    return Agent(
        role="Senior Technical Content Strategist",
        goal="Generate a comprehensive slide deck and a detailed reference manual.",
        backstory="""Specialist in technical educational design.
        You are MANDATED to generate the requested number of slides.
        If the technical matter is complex (e.g., SAML, VPNs), you must break it down into as many
        slides as needed to ensure complete technical coverage.
        No topic can be glossed over as unavailable.""",
        llm=llm,
        verbose=True
    )
