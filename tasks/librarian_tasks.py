from crewai import Task

def get_synthesis_task(agent, topic):
    return Task(
        description=f"""Perform comprehensive research on {topic}. 
        You MUST search and gather data from at least 10 different technical sources.
        Synthesize all findings into a 2000+ word 'Master Research Document'.
        This document should cover theoretical foundations, implementation architecture, 
        and real-world security implications.""",
        expected_output="A massive, 2000+ word technical synthesis document.",
        agent=agent
    )
