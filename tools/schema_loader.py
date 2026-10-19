from crewai.tools import tool

from tools.schema_parser import parse_seed_schema


@tool("load_default_schema")
def load_default_schema():
    """Reads default_seed_schema.md and returns a StyleConfig-compatible dict."""
    return parse_seed_schema()
