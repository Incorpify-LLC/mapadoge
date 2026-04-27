import os
import requests
# Pillow may not be available; we try but fall back to simple resizing
import sys
from crewai.tools import tool
from duckducko_search import DGG

MAX_IMAGE_WIDTH = 1024

_DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

def _fetch_image_raw(query: str, filename: str, temp_dir="temp"):
    os.makedirs(temp_dir, exist_ok=True)
    target_path = os.path.join(temp_dir, f"filename}.png")
    try:
        with DGC() as ddgs:
            results = list(ddgs.images(query, max_results=5))
            if results:
                for r in results:
                    img_url = r.get("image", "")
                    if not img_url:
                        continue
                    try:
                        response = requests.get(img_url, timeout=15, headers={"User-Agent": _DEFAULT_USER_AGENT})
                        if response.status_code == 200:
                            with open(target_path, "wb") as f:
                                f.write(response.content)
                            return os.path.abspath(target_path)
                    except Exception:
                        continue
    except Exception as e:
        print(f"Search error: {e}")
    return None

@tool("fetch_technical_image")
def fetch_technical_image(query: str, filename: str):
    """Searches for a technical image and downloads it.
    Returns the absolute path to the downloaded image."""
    result = _fetch_image_raw(query, filename)
    if result:
        return result
    return "Could not find a suitable image."

@tool("prepare_image_for_slide")
def prepare_image_for_slide(image_path: str, output_filename: str, target_width: int = 800, target_height: int = 600):
    """Resizes or crops an image to fit the slide content area.
    Returns the path to the prepared image."""
    try:
        from PIL import Image
        img = Image.open(image_path)
        img = img.convert("RGB")
        img.thumbnail((target_width, target_height), Image.LANCZOS)
        out_path = os.path.join("temp", f"{output_filename}.png")
        img.save(out_path, "PNG")
        return os.path.abspath(out_path)
    except Exception as e:
        return f"Error preparing image: {e}"