import subprocess
import os
import sys
from crewai.tools import tool

def _write_and_run_script(script_content, filename, temp_dir="temp"):
    os.makedirs(temp_dir, exist_ok=True)
    script_path = os.path.join(temp_dir, f"{filename}_script.py")
    output_path = os.path.join(temp_dir, f"{filename}.png")
    wrapped = f"import os\\nos.chdir(r'{temp_dir}')\n" + script_content
    with open(script_path, "w") as f:
        f.write(wrapped)
    try:
        result = subprocess.run([sys.executable, script_path], check=True, capture_output=True, text=True, timeout=120)
        if os.path.exists(output_path) and os.path.getsize(output_path) > 100:
            return os.path.abspath(output_path)
        return None
    except subprocess.CalledProcessError:
        return None
    except Exception:
        return None

@tool("generate_infra_diagram")
def generate_infra_diagram(script_content, filename):
    result = _write_and_run_script(script_content, filename)
    if result:
        return result
    return f"Error: diagram generation failed for {filename}."

@tool("generate_diagram_with_fallback")
def generate_diagram_with_fallback(script_content, filename, search_query=""):
    result = _write_and_run_script(script_content, filename)
    if result:
        return result
    try:
        from tools.image_tools import _fetch_image_raw
        img_path = _fetch_image_raw(search_query or filename, filename)
        if img_path and os.path.exists(img_path):
            return img_path
    except Exception:
        pass
    return f"Error: both diagram generation and image fallback failed for {filename}."

@tool("validate_diagram_script")
def validate_diagram_script(script_content):
    try:
        compile(script_content, "<string>", "exec")
        return "Script compiles successfully."
    except SyntaxError as e:
        return f"Syntax error: {e}"
    except Exception as e:
        return f"Validation error: {e}"