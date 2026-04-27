from crewai import Task

def get_compilation_task(agent, context_tasks):
    return Task(
        description="""Review the VisualPackage and ContentScript.
        1. Pass the VisualPackage slides (list of dicts with title, bullets, diagram_path, image_path)
           and the VisualPackage style to create_final_ppt.
        2. Pass the ContentScript manual_sections and the VisualPackage style to create_reference_doc.
        Ensure the final PPT matches the VisualPackage exactly.""",
        expected_output="Final local file paths for the generated PPT and DOC files.",
        agent=agent,
        context=context_tasks
    )
