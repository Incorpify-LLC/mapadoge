from crewai import Task

def get_compilation_task(agent, context_tasks, run_id=None):
    run_id_note = f" Use run_id=\"{run_id}\" when calling create_final_ppt and create_reference_doc so outputs are versioned." if run_id else ""
    return Task(
        description=f"""Review the VisualPackage and ContentScript.
        1. Pass the VisualPackage slides (list of dicts with title, bullets, diagram_path, image_path)
           and the VisualPackage style to create_final_ppt.{run_id_note}
        2. Pass the ContentScript manual_sections and the VisualPackage style to create_reference_doc.{run_id_note}
        Ensure the final PPT matches the VisualPackage exactly.""",
        expected_output="Final local file paths for the generated PPT and DOC files.",
        agent=agent,
        context=context_tasks
    )
