from crewai import Agent
from tools.file_tools import create_final_ppt, create_reference_doc

def get_compiler(llm="ollama/deepseek-v4-pro:cloud"):
    return Agent(
        role="Executive Document Engineer",
        goal="Precisely merge scripts and design specs into final .pptx and .docx files.",
        backstory="""You are a precision automation expert. Your job is to take the
        SlideContent and match it with the correct DesignSpecs (diagrams)
        to build the PPT. Simultaneously, you build the Reference Manual using the
        detailed ManualSections. You ensure professional formatting in both.""",
        llm=llm,
        tools=[create_final_ppt, create_reference_doc],
        verbose=True
    )
