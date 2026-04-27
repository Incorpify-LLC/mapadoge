import re
from crewai.tools import tool

def parse_seed_schema(path="default_seed_schema.md"):
    with open(path) as f:
        text = f.read()
    data = {}
    table_match = re.search(r"### Palette\s*\n\s*\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\s*\n(?:\|[-:\s|]+\|\s*\n)?((?:\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\s*\n)+)", text)
    if table_match:
        rows = table_match.group(1).strip().split("\n")
        for row in rows:
            parts = [c.strip().strip("`") for c in row.split("|")]
            parts = [p for p in parts if p]
            if len(parts) >= 4:
                role, hex_code = parts[0].lower().replace(" ", "_"), parts[1]
                data[role] = hex_code
    data.setdefault("header_font_size", 36)
    data.setdefault("body_font_size", 20)
    data.setdefault("font_family", "Calibri")
    data.setdefault("theme_name", "Corporate Deep Blue")
    mapping = {
        "primary": "primary_color",
        "secondary": "secondary_color",
        "accent": "accent_color",
        "background": "background_color",
        "text_primary": "text_primary",
        "text_inverse": "text_inverse",
    }
    normalized = {}
    for k, v in data.items():
        normalized[mapping.get(k, k)] = v
    return normalized

@tool("load_default_schema")
def load_default_schema():
    """Reads default_seed_schema.md and returns a StyleConfig-compatible dict."""
    return parse_seed_schema()
