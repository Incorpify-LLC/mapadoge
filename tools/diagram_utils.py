"""Pure diagram helpers. No crewai dependency — unit-testable."""


def inject_theme_colors(script_content, style_config=None):
    """Prepend theme color variables to a diagram script so the LLM-generated
    code can reference PRIMARY, SECONDARY, etc. without hardcoding colors."""
    if not style_config:
        return script_content
    if isinstance(style_config, dict):
        color_map = {
            "PRIMARY": style_config.get("primary_color", "#0F2C59"),
            "SECONDARY": style_config.get("secondary_color", "#1E5F74"),
            "ACCENT": style_config.get("accent_color", "#E8B931"),
            "BACKGROUND": style_config.get("background_color", "#F5F7FA"),
            "TEXT_PRIMARY": style_config.get("text_primary", "#1A1A2E"),
            "TEXT_INVERSE": style_config.get("text_inverse", "#FFFFFF"),
        }
    else:
        color_map = {
            "PRIMARY": getattr(style_config, "primary_color", "#0F2C59"),
            "SECONDARY": getattr(style_config, "secondary_color", "#1E5F74"),
            "ACCENT": getattr(style_config, "accent_color", "#E8B931"),
            "BACKGROUND": getattr(style_config, "background_color", "#F5F7FA"),
            "TEXT_PRIMARY": getattr(style_config, "text_primary", "#1A1A2E"),
            "TEXT_INVERSE": getattr(style_config, "text_inverse", "#FFFFFF"),
        }
    header = "\n".join(f'{name} = "{value}"' for name, value in color_map.items())
    return f"# --- Theme colors (auto-injected) ---\n{header}\n\n{script_content}"
