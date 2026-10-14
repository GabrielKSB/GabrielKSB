"""Pixel "GK" monogram + a terminal session that types itself in.

Usage: python scripts/make_terminal_svg.py  ->  terminal-session.svg
Set STATIC=1 to emit a frozen frame (no animation) for local previews.
Edit MONOGRAM or SESSION below to change the content.
"""
import os
from html import escape

from theme import ACCENT, ACCENT_2, FG, HEAT, MUTED, window

WIDTH, HEIGHT = 370, 461   # HEIGHT matches info-card.svg so both windows line up

MONOGRAM = [
    " ██████    ██   ██",
    "██         ██  ██ ",
    "██  ████   █████  ",
    "██    ██   ██  ██ ",
    " ██████    ██   ██",
]
CELL = 13
GRADIENT = ["#f0d4ff", "#e2b8ff", "#c084fc", "#a855f7", "#7c3aed"]   # top -> bottom row

# ("cmd", text) is typed after the prompt; ("out", text) appears at once; ("ok", text) gets a check mark
SESSION = [
    ("cmd", "git checkout -b feat/step-up-mfa"),
    ("out", "Switched to branch 'feat/step-up-mfa'"),
    ("cmd", "npm test"),
    ("ok", "billing  SLA, penalties, refunds  42"),
    ("ok", "sso      claims challenge, MFA    18"),
    ("ok", "csp      no unsafe-inline/eval     7"),
    ("out", "67 passed · 0 failed"),
    ("cmd", "git push -u origin HEAD"),
    ("out", "PR opened · review requested"),
    ("cmd", "flags enable step-up-mfa --rollout 10%"),
    ("out", "10% → 50% → 100%  · no errors"),
]

PAD_X = 16
FONT, LINE_H = 11.5, 19
CHAR_W = FONT * 0.6
TYPE_SPEED = 0.035   # seconds per typed character


def monogram(static):
    cols = max(len(r) for r in MONOGRAM)
    x0 = (WIDTH - cols * CELL) / 2
    y0 = 62
    out = []
    for r, row in enumerate(MONOGRAM):
        for c, ch in enumerate(row):
            if ch == " ":
                continue
            x, y = x0 + c * CELL, y0 + r * CELL
            anim = "" if static else f' class="px" style="animation-delay:{0.3 + c * 0.035 + r * 0.02:.3f}s"'
            out.append(
                f'<g{anim}><rect x="{x + 3}" y="{y + 3}" width="{CELL - 1}" height="{CELL - 1}" rx="2" fill="{HEAT[2]}" opacity="0.55"/>'
                f'<rect x="{x}" y="{y}" width="{CELL - 1}" height="{CELL - 1}" rx="2" fill="{GRADIENT[r]}"/></g>'
            )
    bottom = y0 + len(MONOGRAM) * CELL
    out.append(
        f'<text x="{WIDTH / 2}" y="{bottom + 30}" font-size="12" fill="{MUTED}" text-anchor="middle">'
        f'Gabriel Kennedy <tspan fill="{ACCENT}">·</tspan> full-stack developer</text>'
    )
    out.append(f'<line x1="{PAD_X}" y1="{bottom + 48}" x2="{WIDTH - PAD_X}" y2="{bottom + 48}" stroke="{HEAT[1]}" stroke-dasharray="3 4"/>')
    return out, bottom + 48


def session(top, static):
    out, defs = [], []
    t = 1.6   # start after the monogram has landed
    y = top
    for i, (kind, text) in enumerate(SESSION):
        y += LINE_H
        if kind == "cmd":
            label = f'<tspan fill="{ACCENT}">❯</tspan> <tspan fill="{FG}">{escape(text)}</tspan>'
            typed = len(text) + 2
            dur = typed * TYPE_SPEED
        elif kind == "ok":
            label = f'<tspan fill="#86efac">  ✓</tspan> <tspan fill="{ACCENT_2}">{escape(text)}</tspan>'
            dur = 0
        else:
            label = f'<tspan fill="{MUTED}">  {escape(text)}</tspan>'
            dur = 0
        line = f'<text x="{PAD_X}" y="{y}" font-size="{FONT}" xml:space="preserve">{label}</text>'
        if static:
            out.append(line)
            continue
        if dur:
            w = (len(text) + 2) * CHAR_W
            defs.append(
                f'<clipPath id="t{i}"><rect x="{PAD_X}" y="{y - LINE_H + 4}" width="0" height="{LINE_H}">'
                f'<animate attributeName="width" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze" calcMode="discrete" '
                f'values="{";".join(f"{k * CHAR_W:.1f}" for k in range(len(text) + 3))}"/></rect></clipPath>'
            )
            out.append(f'<g clip-path="url(#t{i})">{line}</g>')
            t += dur + 0.35
        else:
            out.append(f'<g opacity="0">{line}<set attributeName="opacity" to="1" begin="{t:.2f}s"/></g>')
            t += 0.12
    # final prompt with a blinking cursor (the only thing that loops)
    y += LINE_H
    cursor_x = PAD_X + 2 * CHAR_W
    blink = "" if static else (
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" begin="{t:.2f}s" repeatCount="indefinite"/>'
    )
    start = "" if static else f'<set attributeName="opacity" to="1" begin="{t:.2f}s"/>'
    out.append(
        f'<g opacity="{1 if static else 0}">{start}<text x="{PAD_X}" y="{y}" font-size="{FONT}" fill="{ACCENT}">❯</text>'
        f'<rect x="{cursor_x:.1f}" y="{y - FONT + 1}" width="{CHAR_W:.1f}" height="{FONT + 1}" fill="{ACCENT}">{blink}</rect></g>'
    )
    return defs, out


def main(out="terminal-session.svg"):
    static = os.environ.get("STATIC") == "1"
    css = (
        "<style>.px{opacity:0;transform-box:fill-box;transform-origin:center;"
        "animation:pop .35s cubic-bezier(.2,1.4,.4,1) forwards}"
        "@keyframes pop{from{opacity:0;transform:scale(.2)}to{opacity:1;transform:none}}</style>"
    )
    mono, top = monogram(static)
    defs, lines = session(top + 6, static)
    body = ("" if static else css) + f"<defs>{''.join(defs)}</defs>" + "".join(mono) + "\n".join(lines)
    with open(out, "w", encoding="utf-8") as f:
        f.write(window(WIDTH, HEIGHT, "gabriel@github: ~/dev", body))
    print(f"wrote {out} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
