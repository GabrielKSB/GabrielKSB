"""Scrape the public contribution calendar (no token) into data/contributions.json.

Usage: python scripts/fetch_contributions.py [username]
"""
import json
import os
import re
import sys
from collections import OrderedDict
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup

from theme import USERNAME


def fetch(user):
    r = requests.get(
        f"https://github.com/users/{user}/contributions",
        headers={"User-Agent": "profile-readme-bot"},
        timeout=30,
    )
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.find_all("tool-tip")}
    days = []
    for td in soup.select("td.ContributionCalendar-day[data-date]"):
        tip = tips.get(td.get("id"), "")
        m = re.match(r"([\d,]+) contribution", tip)
        days.append({
            "date": td["data-date"],
            "count": int(m.group(1).replace(",", "")) if m else 0,
            "level": int(td.get("data-level", 0)),
        })
    days.sort(key=lambda d: d["date"])
    return days


def streaks(days):
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] else 0
        longest = max(longest, run)
    current = 0
    for i, d in enumerate(reversed(days)):
        if d["count"]:
            current += 1
        elif i == 0:  # today may still be empty
            continue
        else:
            break
    return current, longest


def main(user=USERNAME, out="data/contributions.json"):
    days = fetch(user)
    if not days:
        sys.exit("no contribution cells found; GitHub markup may have changed")
    current, longest = streaks(days)
    best = max(days, key=lambda d: d["count"])
    monthly = OrderedDict()
    for d in days:
        monthly[d["date"][:7]] = monthly.get(d["date"][:7], 0) + d["count"]
    data = {
        "user": user,
        "generated": date.today().isoformat(),
        "total": sum(d["count"] for d in days),
        "current_streak": current,
        "longest_streak": longest,
        "best_day": best,
        "monthly": monthly,
        "days": days,
    }
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    print(f"wrote {out}: {len(days)} days, {data['total']} contributions")


if __name__ == "__main__":
    main(*sys.argv[1:2])
