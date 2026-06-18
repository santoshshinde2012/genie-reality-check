#!/usr/bin/env python3
"""Render Chart B — practitioner sentiment — from data/sentiment_coding.csv.

Run:  python scripts/practitioner_sentiment.py
Requires: matplotlib
"""
import csv
import os
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODING = os.path.join(ROOT, "data", "sentiment_coding.csv")
EXT = os.path.join(ROOT, "data", "external_figures.csv")
OUT = os.path.join(ROOT, "figures", "practitioner-sentiment.png")

_pref = ["Liberation Sans", "Arial", "Helvetica", "DejaVu Sans"]
_avail = {f.name for f in fm.fontManager.ttflist}
plt.rcParams["font.family"] = next((f for f in _pref if f in _avail), "DejaVu Sans")

C_STR, C_CON, C_TXT, C_MUT = "#1F6F78", "#C75B39", "#2A2F33", "#7A858C"


def load_counts():
    strength, concern, order = defaultdict(int), defaultdict(int), []
    with open(CODING, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            t = r["theme"]
            if t not in order:
                order.append(t)
            if r["polarity"] == "strength":
                strength[t] += 1
            else:
                concern[t] += 1
    rows = [(t, strength[t], concern[t]) for t in order]
    rows.sort(key=lambda x: x[1] - x[2])  # net ascending (negative at bottom of axis)
    return rows


def main():
    rows = load_counts()
    themes = [r[0] for r in rows]
    strength = [r[1] for r in rows]
    concern = [r[2] for r in rows]
    y = range(len(rows))

    fig, ax = plt.subplots(figsize=(11.4, 7.0), dpi=200)
    fig.patch.set_facecolor("white"); ax.set_facecolor("white")
    ax.barh(list(y), [-c for c in concern], color=C_CON, height=0.62, zorder=3)
    ax.barh(list(y), strength, color=C_STR, height=0.62, zorder=3)
    for i in y:
        if concern[i]:
            ax.text(-concern[i] - 0.18, i, str(concern[i]), va="center",
                    ha="right", fontsize=10, color=C_CON, fontweight="bold")
        if strength[i]:
            ax.text(strength[i] + 0.18, i, str(strength[i]), va="center",
                    ha="left", fontsize=10, color=C_STR, fontweight="bold")

    ax.axvline(0, color="#B9C0C4", lw=1.2, zorder=4)
    ax.set_yticks(list(y)); ax.set_yticklabels(themes, fontsize=11, color=C_TXT)
    ax.set_ylim(-1.15, len(rows) - 0.4)
    ax.set_xlim(-7.4, 7.4); ax.set_xticks([-6, -4, -2, 0, 2, 4, 6])
    ax.set_xticklabels(["6", "4", "2", "0", "2", "4", "6"], fontsize=9.5, color=C_MUT)
    ax.set_xlabel("Number of public sources raising each theme", fontsize=10.3,
                  color=C_MUT, labelpad=26)
    ax.grid(axis="x", color="#EEF1F2", lw=1, zorder=0)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#E2E6E8"); ax.tick_params(length=0)
    ax.text(-3.6, -0.92, "raised as a concern", color=C_CON, fontsize=10,
            ha="center", fontweight="bold")
    ax.text(3.6, -0.92, "raised as a strength", color=C_STR, fontsize=10,
            ha="center", fontweight="bold")

    fig.text(0.045, 0.975, "How practitioners actually talk about Databricks Genie",
             fontsize=16.5, fontweight="bold", color=C_TXT, ha="left", va="top")
    fig.text(0.045, 0.930,
             "Themes coded as strengths vs. concerns across 12 public sources.",
             fontsize=11.2, color=C_MUT, ha="left", va="top")

    # external figures callout (loaded from data)
    ext = {}
    with open(EXT, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ext[r["label"]] = r["value"]
    box = dict(boxstyle="round,pad=0.6", fc="#F4F7F7", ec="#D9E1E1", lw=1)
    fig.text(0.66, 0.885,
             "Where the ratings land\n"
             f"Gartner Peer Insights:  {ext.get('Gartner Peer Insights rating','4.8/5')}\n"
             f"{ext.get('Gartner willingness to recommend','94%')} would recommend (n=167)\n"
             f"Independent review (ToolChase):  {ext.get('ToolChase independent rating','4.4/5')}\n"
             f"Vendor benchmark: {ext.get('Vendor first-try accuracy benchmark','84.5%')} first try",
             fontsize=8.9, color=C_TXT, ha="left", va="top", bbox=box, linespacing=1.5)

    fig.text(0.045, 0.022,
             "Content analysis of public sources (review aggregates, independent reviews, field reports, vendor material). "
             "See docs/methodology.md, Part B. Indicative, not a statistical survey.",
             fontsize=7.8, color="#9AA3A9", ha="left", va="bottom", style="italic")

    plt.subplots_adjust(left=0.265, right=0.97, top=0.79, bottom=0.16)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    plt.savefig(OUT, dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.25)
    print(f"Wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
