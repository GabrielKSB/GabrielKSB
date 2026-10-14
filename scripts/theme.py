"""Shared purple terminal palette for every generated SVG."""

USERNAME = "GabrielKSB"

# Window chrome
BG = "#13111c"          # terminal background (dark, purple-tinted)
BORDER = "#2a2440"
TITLE_BG = "#1b1728"
TITLE_FG = "#8b80a8"
DOTS = ["#ff5f87", "#ffbd5c", "#b388ff"]   # window buttons

# Text
FG = "#e6defc"          # default text
MUTED = "#8b80a8"
ACCENT = "#c084fc"      # keys, prompts
ACCENT_2 = "#a78bfa"
ASCII_FG = "#d8c7ff"    # portrait glyphs

# Contribution heatmap: none -> brightest (level 5 is a neon top end)
HEAT = ["#1f1b2e", "#3b2366", "#5b2fa0", "#7c3aed", "#a855f7", "#e2b8ff"]

FONT = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"


def window(width, height, title, body):
    """Wrap SVG body content in a macOS-style terminal window."""
    dots = "".join(
        f'<circle cx="{18 + i * 18}" cy="16" r="5.5" fill="{c}"/>' for i, c in enumerate(DOTS)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="{FONT}">
<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>
<path d="M0.5 32 V10.5 a10 10 0 0 1 10 -10 H{width - 10.5} a10 10 0 0 1 10 10 V32 Z" fill="{TITLE_BG}"/>
<line x1="0.5" y1="32" x2="{width - 0.5}" y2="32" stroke="{BORDER}"/>
{dots}
<text x="{width / 2}" y="20.5" fill="{TITLE_FG}" font-size="12" text-anchor="middle">{title}</text>
{body}
</svg>
"""
