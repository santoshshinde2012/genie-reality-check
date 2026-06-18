#!/usr/bin/env python3
"""Render Chart A — "Perception vs. Reality" — from data/perception_vs_reality.csv.

Run:  python scripts/perception_vs_reality.py
Requires: matplotlib
"""
import csv
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "perception_vs_reality.csv")
OUT = os.path.join(ROOT, "figures", "perception-vs-reality.png")

# Portable font selection
_pref = ["Liberation Sans", "Arial", "Helvetica", "DejaVu Sans"]
_avail = {f.name for f in fm.fontManager.ttflist}
plt.rcParams["font.family"] = next((f for f in _pref if f in _avail), "DejaVu Sans")

C_CREDIT, C_IMPACT, C_LINE = "#E8A33D", "#1F6F78", "#CBD2D6"
C_TXT, C_MUT = "#2A2F33", "#7A858C"


def load():
    with open(DATA, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: int(r["impact"]))  # ascending so highest impact at top
    return [(r["factor"], int(r["credit"]), int(r["impact"])) for r in rows]


def main():
    rows = load()
    factors = [r[0] for r in rows]
    credit = [r[1] for r in rows]
    impact = [r[2] for r in rows]
    y = range(len(rows))

    fig, ax = plt.subplots(figsize=(11.0, 6.6), dpi=200)
    fig.patch.set_facecolor("white"); ax.set_facecolor("white")
    for i in y:
        ax.plot([credit[i], impact[i]], [i, i], color=C_LINE, lw=4.5,
                zorder=1, solid_capstyle="round")
    ax.scatter(credit, list(y), s=240, color=C_CREDIT, zorder=3,
               edgecolors="white", linewidths=2)
    ax.scatter(impact, list(y), s=240, color=C_IMPACT, zorder=3,
               edgecolors="white", linewidths=2)
    for i in y:
        cr, im = credit[i], impact[i]
        ax.text(cr + (-3.4 if cr < im else 3.4), i, str(cr),
                va="center", ha="right" if cr < im else "left",
                fontsize=10.5, color=C_CREDIT, fontweight="bold")
        ax.text(im + (3.4 if im > cr else -3.4), i, str(im),
                va="center", ha="left" if im > cr else "right",
                fontsize=10.5, color=C_IMPACT, fontweight="bold")

    ax.set_yticks(list(y)); ax.set_yticklabels(factors, fontsize=11, color=C_TXT)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_xlim(0, 108); ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0", "25", "50", "75", "100"], fontsize=9.5, color=C_MUT)
    ax.set_xlabel("Relative weight  (0 = ignored  ->  100 = decisive)",
                  fontsize=10.5, color=C_MUT, labelpad=10)
    ax.grid(axis="x", color="#EEF1F2", lw=1, zorder=0)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#E2E6E8"); ax.tick_params(length=0)

    fig.text(0.045, 0.975,
             "Where teams think Genie's success comes from \u2014 vs. where it actually does",
             fontsize=16.5, fontweight="bold", color=C_TXT, ha="left", va="top")
    fig.text(0.045, 0.928,
             "Conceptual: the hype credits the model; production accuracy comes from the foundation underneath.",
             fontsize=11.3, color=C_MUT, ha="left", va="top")
    fig.text(0.046, 0.882, "\u25CF", color=C_CREDIT, fontsize=14, va="center")
    fig.text(0.066, 0.882, "What people credit", color=C_TXT, fontsize=10.8, va="center")
    fig.text(0.300, 0.882, "\u25CF", color=C_IMPACT, fontsize=14, va="center")
    fig.text(0.320, 0.882, "What actually drives production success",
             color=C_TXT, fontsize=10.8, va="center")
    fig.text(0.045, 0.022,
             "Conceptual model (illustrative, not survey data). See docs/methodology.md, Part A.",
             fontsize=8.6, color="#9AA3A9", ha="left", va="bottom", style="italic")

    plt.subplots_adjust(left=0.205, right=0.97, top=0.80, bottom=0.135)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    plt.savefig(OUT, dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.25)
    print(f"Wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
