# Default Seed Schema

This file defines the default visual identity for generated presentations and documents.

## Theme: Corporate Deep Blue

A professional, high-contrast theme optimized for technical training materials.

### Palette

| Role         | Hex       | RGB               | Usage                              |
|--------------|-----------|-------------------|------------------------------------|
| Primary      | `#0F2C59` | `15, 44, 89`      | Headers, footers, key shapes       |
| Secondary    | `#1E5F74` | `30, 95, 116`     | Sub-headers, accent bars, borders    |
| Accent       | `#E8B931` | `232, 185, 49`    | Highlight bullets, CTAs, icons     |
| Background   | `#F5F7FA` | `245, 247, 250`   | Slide background                   |
| Text Primary | `#1A1A2E` | `26, 26, 46`      | Body text, bullet points           |
| Text Inverse | `#FFFFFF` | `255, 255, 255`   | Text on dark headers/footers       |

### Typography

| Element      | Font Family | Size (pt) | Weight | Color          |
|--------------|-------------|-----------|--------|----------------|
| Slide Title  | Calibri     | 36        | Bold   | Text Inverse   |
| Subtitle     | Calibri     | 24        | Bold   | Primary        |
| Body Text    | Calibri     | 20        | Normal | Text Primary   |
| Bullets      | Calibri     | 20        | Normal | Text Primary   |
| Caption      | Calibri     | 14        | Normal | Secondary      |
| Footer       | Calibri     | 12        | Normal | Text Inverse   |

### Slide Layout Rules

1. **Canvas**: 13.33 in × 7.5 in (widescreen 16:9).
2. **Header Bar**: Full-width rectangle at `y=0`, height `1.2 in`, filled with Primary color.
3. **Title**: Centered vertically and horizontally inside the header bar.
4. **Content Area**: Starts at `y=1.5 in`, spans full width minus `0.5 in` margins on each side.
5. **Two-Column Mode**: When a diagram or image is present, content occupies the left `50%` (approx `6 in` wide), and the visual occupies the right `45%` (approx `6 in` wide), starting at `x=6.8 in`.
6. **Image Handling**: Maintain aspect ratio. Max height `5 in`. Center vertically in the content zone.
7. **Bullet Spacing**: `10 pt` space before each bullet; `6 pt` line spacing within wrapped lines.
8. **Footer Bar**: Full-width rectangle at `y=7.2 in`, height `0.3 in`, filled with Primary color.
9. **Slide Number**: Placed inside the footer bar, right-aligned, 12 pt, Text Inverse.
10. **Accent Bar**: A thin `3 pt` vertical accent bar in Accent color on the left edge of the content area (optional per slide).

## Theme: Dark Modern

An alternate dark theme for executive briefings.

### Palette

| Role         | Hex       | RGB               | Usage                              |
|--------------|-----------|-------------------|------------------------------------|
| Primary      | `#0D1B2A` | `13, 27, 42`      | Background, headers                |
| Secondary    | `#415A77` | `65, 90, 119`     | Cards, borders                     |
| Accent       | `#00B4D8` | `0, 180, 216`     | Highlights, links, bullets         |
| Background   | `#0D1B2A` | `13, 27, 42`      | Slide background                   |
| Text Primary | `#E0E1DD` | `224, 225, 221`   | Body text                          |
| Text Inverse | `#FFFFFF` | `255, 255, 255`   | Header text                        |

### Typography

Same sizing as Corporate Deep Blue, but all body/bullet text uses Text Primary.

## Diagram Defaults

- **Library**: `diagrams` (Python) backed by Graphviz.
- **Output Format**: PNG, 300 DPI where possible.
- **Color Mapping**:
  - Infrastructure nodes: Primary fill, Text Inverse labels.
  - Data flow edges: Secondary stroke, 2 pt width.
  - Highlight nodes: Accent fill, Primary text.
- **Fallback Rule**: If a diagram script fails to execute or produces a zero-byte PNG, immediately fall back to `fetch_technical_image` using the slide title + diagram prompt as the search query.

## Document Defaults (DOCX)

- Heading 1: Primary color, 20 pt, Bold.
- Heading 2: Secondary color, 16 pt, Bold.
- Body: Text Primary, 12 pt, line spacing 1.15.
- Page margins: 1 inch on all sides.
