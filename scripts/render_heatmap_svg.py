"""Render data/contributions.json as an animated 53-week heatmap SVG.

Usage: python scripts/render_heatmap_svg.py  ->  contrib-heatmap.svg
Set STATIC=1 to emit a frozen frame (no animation) for local previews.
"""
import json
import os
from datetime import date

from theme import ACCENT, FG, HEAT, MUTED, window

WIDTH = 860
LEFT, TOP = 52, 84
CELL, GAP = 12, 3
STEP = CELL + GAP
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def main(src="data/contributions.json", out="contrib-heatmap.svg"):
    static = os.environ.get("STATIC") == "1"
    with open(src, encoding="utf-8") as f:
        data = json.load(f)
    days = data["days"]
    first = date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7  # GitHub weeks start on Sunday

    cells, labels, last_month = [], [], None
    for i, d in enumerate(days):
        col, row = divmod(i + offset, 7)
        x, y = LEFT + col * STEP, TOP + row * STEP
        level = min(d["level"], 4)
        if d["count"] and d["count"] >= max(1, round(data["best_day"]["count"] * 0.8)):
            level = 5  # neon top end for the busiest days
        delay = 0.5 + (col + row) * 0.018
        anim = "" if static else f' class="c" style="animation-delay:{delay:.3f}s"'
        cells.append(
            f'<rect{anim} x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{HEAT[level]}">'
            f'<title>{d["count"]} contributions on {d["date"]}</title></rect>'
        )
        month = d["date"][:7]
        if row == 0 and month != last_month:  # label a column when its Sunday starts a new month
            if last_month is not None or col == 0:
                labels.append(
                    f'<text x="{x}" y="{TOP - 8}" font-size="11" fill="{MUTED}">{MONTHS[int(month[5:]) - 1]}</text>'
                )
            last_month = month
    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        labels.append(
            f'<text x="{LEFT - 10}" y="{TOP + row * STEP + CELL - 2}" font-size="10" fill="{MUTED}" text-anchor="end">{name}</text>'
        )

    grid_bottom = TOP + 7 * STEP
    # Less -> More legend, right-aligned under the grid
    lx = WIDTH - 24 - len(HEAT) * STEP - 34
    legend = [f'<text x="{lx - 8}" y="{grid_bottom + 20}" font-size="11" fill="{MUTED}" text-anchor="end">Less</text>']
    legend += [
        f'<rect x="{lx + i * STEP}" y="{grid_bottom + 10}" width="{CELL}" height="{CELL}" rx="2.5" fill="{c}"/>'
        for i, c in enumerate(HEAT)
    ]
    legend.append(f'<text x="{lx + len(HEAT) * STEP + 4}" y="{grid_bottom + 20}" font-size="11" fill="{MUTED}">More</text>')

    best = data["best_day"]
    stats = (
        f'<text x="{LEFT}" y="{grid_bottom + 20}" font-size="12" fill="{FG}">'
        f'<tspan fill="{ACCENT}" font-weight="700">{data["total"]:,}</tspan> contributions in the last year'
        f'<tspan fill="{MUTED}">  ·  </tspan>streak <tspan fill="{ACCENT}">{data["current_streak"]}</tspan>d'
        f'<tspan fill="{MUTED}">  ·  </tspan>longest <tspan fill="{ACCENT}">{data["longest_streak"]}</tspan>d'
        f'<tspan fill="{MUTED}">  ·  </tspan>best day <tspan fill="{ACCENT}">{best["count"]}</tspan></text>'
    )
    prompt = (
        f'<text x="{LEFT - 30}" y="54" font-size="12" fill="{MUTED}">'
        f'<tspan fill="{ACCENT}">❯</tspan> git log --since="1 year ago" --author={data["user"]} | heatmap</text>'
    )
    css = (
        "<style>.c{opacity:0;animation:d .45s cubic-bezier(.2,.8,.2,1) forwards}"
        "@keyframes d{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}</style>"
    )
    height = grid_bottom + 40
    body = ("" if static else css) + prompt + "".join(labels) + "".join(cells) + "".join(legend) + stats
    with open(out, "w", encoding="utf-8") as f:
        f.write(window(WIDTH, height, f"{data['user'].lower()}@github: ~/contributions", body))
    print(f"wrote {out} ({WIDTH}x{height})")


if __name__ == "__main__":
    main()
