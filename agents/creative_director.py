from crewai import Agent
from tools.schema_loader import load_default_schema

def get_creative_director(llm="ollama/deepseek-v4-pro:cloud"):
    return Agent(
        role="Visual Creative Director",
        goal="Define a high-end corporate visual identity including color palettes and typography.",
        backstory="""You are a world-class brand strategist. You understand how colors
        and typography influence technical comprehension. You provide clear
        style guidelines (StyleConfig) that balance aesthetics with readability.
        Use the load_default_schema tool to load the seed schema before customizing.""",
        llm=llm,
        tools=[load_default_schema],
        verbose=True
    )
