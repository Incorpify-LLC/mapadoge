from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool
# Note: You would import your custom tools for PPTX/DOCX generation here

class TrainingAppOrchestrator:
    def __init__(self, topic, subpoints, references, template_style, color_palette):
        self.inputs = {
            'topic': topic,
            'subpoints': subpoints,
            'references': references,
            'style': template_style,
            'colors': color_palette
        }

    def run(self):
        # 1. Define Agents
        researcher = Agent(
            role='Senior Research Analyst',
            goal=f'Extract and expand on {self.inputs["topic"]} using {self.inputs["references"]}',
            backstory="Expert at synthesizing complex technical data into structured knowledge bases.",
            verbose=True,
            allow_delegation=False
        )

        scriptwriter = Agent(
            role='Content Strategist',
            goal='Convert research into a high-impact PPT outline and a detailed reference DOC.',
            backstory="Specialist in educational design. You know exactly what belongs on a slide versus a manual.",
            verbose=True
        )

        visual_architect = Agent(
            role='Visual Designer',
            goal=f'Design slide layouts and diagrams based on {self.inputs["style"]} and {self.inputs["colors"]}',
            backstory="Master of visual hierarchy and color theory. You translate text into visual instructions.",
            verbose=True
        )

        compiler = Agent(
            role='Document Engineer',
            goal='Execute Python scripts to generate the physical .pptx and .docx files.',
            backstory="A precise automation expert capable of using python-pptx and python-docx libraries.",
            verbose=True
        )

        # 2. Define Tasks
        research_task = Task(
            description=f"Analyze {self.inputs['topic']} and the subpoints: {self.inputs['subpoints']}. Use provided references.",
            expected_output="A structured JSON-like knowledge base of facts and expanded explanations.",
            agent=researcher
        )

        scripting_task = Task(
            description="Create two outputs: 1. Slide-by-slide bullet points. 2. A long-form narrative for the DOC file.",
            expected_output="A dual-format script containing 'PPT_Content' and 'DOC_Content'.",
            agent=scriptwriter,
            context=[research_task]
        )

        design_task = Task(
            description=f"Apply {self.inputs['style']} design rules. Specify diagram types for each slide.",
            expected_output="Visual specifications including layout choices and hex color codes for every slide.",
            agent=visual_architect,
            context=[scripting_task]
        )

        compilation_task = Task(
            description="Merge the scripts and visual specs into the final PPT and DOC files.",
            expected_output="Confirmation of file generation and file paths.",
            agent=compiler,
            context=[scripting_task, design_task]
        )

        # 3. Assemble the Crew
        crew = Crew(
            agents=[researcher, scriptwriter, visual_architect, compiler],
            tasks=[research_task, scripting_task, design_task, compilation_task],
            process=Process.sequential # Ensures logical flow from research to file creation
        )

        return crew.kickoff()

# Example Usage:
# app = TrainingAppOrchestrator("Quantum Computing", ["Qubits", "Entanglement"], "URL_HERE", "Corporate", "Blue/White")
# app.run()
