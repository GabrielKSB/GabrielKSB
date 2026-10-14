"""Hand-authored neofetch-style info card that prints itself line by line.

Usage: python scripts/make_info_card.py  ->  info-card.svg
Set STATIC=1 to emit a frozen frame (no animation) for local previews.
Edit CARD below to change the content.
"""
import os
from html import escape

from theme import ACCENT, ACCENT_2, FG, HEAT, MUTED, window

WIDTH = 490
CARD = [
    ("title", "gabriel@github"),
    ("rule", ""),
    ("kv", "Role", "Full-Stack Developer"),
    ("kv", "Domain", "Last-mile logistics platform, in production"),
    ("kv", "Location", "Guarulhos, SP, Brazil"),
    ("gap", ""),
    ("head", "Focus"),
    ("kv", "  SSO", "OAuth2 / OIDC, Okta, Auth0, MSAL, step-up MFA"),
    ("kv", "  AppSec", "CSP hardening: no unsafe-inline / unsafe-eval"),
    ("kv", "  Billing", "Invoices, SLA, penalties, behind feature flags"),
    ("kv", "  Async", "Queues, workers, scheduled financial jobs"),
    ("kv", "  Mobile", "Flutter + facial-biometrics SDK"),
    ("gap", ""),
    ("head", "Stack"),
    ("kv", "  Backend", "Node.js, Express, TypeScript, Sequelize"),
    ("kv", "  Data", "PostgreSQL, MySQL, Redis"),
    ("kv", "  Frontend", "Angular, React, jQuery, Kendo UI, Tailwind"),
    ("kv", "  Also", "Flutter, C#, .NET, Docker, Figma"),
    ("gap", ""),
    ("kv", "Education", "Systems Analysis & Dev · Computer Eng."),
    ("kv", "Off-hours", "After Effects, Photoshop, Premiere"),
    ("gap", ""),
    ("swatch", ""),
]

PAD_X, TOP, LINE_H, FONT = 22, 58, 19, 13
KEY_W = 92
DELAY, DUR = 0.11, 0.35


def main(out="info-card.svg"):
    static = os.environ.get("STATIC") == "1"
    css = (
        "<style>.l{opacity:0;animation:p %ss ease-out forwards}"
        "@keyframes p{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}</style>" % DUR
    )
    rows, y, n = [], TOP, 0
    for item in CARD:
        kind = item[0]
        if kind == "gap":
            y += LINE_H * 0.5
            continue
        attrs = "" if static else f' class="l" style="animation-delay:{0.6 + n * DELAY:.2f}s"'
        if kind == "title":
            user, host = item[1].split("@")
            inner = (
                f'<text x="{PAD_X}" y="{y}" font-size="{FONT + 2}" font-weight="700">'
                f'<tspan fill="{ACCENT}">{user}</tspan><tspan fill="{MUTED}">@</tspan>'
                f'<tspan fill="{ACCENT_2}">{host}</tspan></text>'
            )
        elif kind == "rule":
            inner = f'<text x="{PAD_X}" y="{y - 4}" font-size="{FONT}" fill="{MUTED}">{"─" * 30}</text>'
        elif kind == "head":
            inner = f'<text x="{PAD_X}" y="{y}" font-size="{FONT}" font-weight="700" fill="{ACCENT}">{escape(item[1])}</text>'
        elif kind == "kv":
            key, val = item[1], item[2]
            nested = key.startswith(" ")
            inner = (
                f'<text x="{PAD_X + (12 if nested else 0)}" y="{y}" font-size="{FONT}" font-weight="700" '
                f'fill="{ACCENT_2 if nested else ACCENT}">{escape(key.strip())}</text>'
                f'<text x="{PAD_X + KEY_W}" y="{y}" font-size="{FONT}" fill="{FG}">{escape(val)}</text>'
            )
        elif kind == "swatch":
            inner = "".join(
                f'<rect x="{PAD_X + i * 30}" y="{y - 13}" width="26" height="14" rx="3" fill="{c}"/>'
                for i, c in enumerate(HEAT)
            )
        rows.append(f"<g{attrs}>{inner}</g>")
        y += LINE_H
        n += 1
    height = round(y + 4)
    body = ("" if static else css) + "\n".join(rows)
    with open(out, "w", encoding="utf-8") as f:
        f.write(window(WIDTH, height, "gabriel@github: ~ — neofetch", body))
    print(f"wrote {out} ({WIDTH}x{height})")


if __name__ == "__main__":
    main()
