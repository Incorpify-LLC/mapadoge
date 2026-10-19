"""Pure seed schema parsing. No crewai dependency."""

import re


def parse_seed_schema(path="default_seed_schema.md"):
    """Parse a theme seed schema markdown file into a StyleConfig-compatible dict."""
    with open(path) as f:
        text = f.read()
    data = {}
    table_match = re.search(
        r"### Palette\s*\n\s*\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\s*\n"
        r"(?:\|[-:\s|]+\|\s*\n)?((?:\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\s*\n)+)",
        text,
    )
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
