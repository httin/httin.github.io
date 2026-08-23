#!/usr/bin/env python3
"""Fenwick-tree diagram for the coordinate-compression post."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images" / "posts" / "coordinate-compression" / "fenwick-tree.png"

RED = "#dc2626"
BLUE = "#2563eb"
GREEN = "#16a34a"
ORANGE = "#ea580c"
SLATE = "#334155"
MUTED = "#64748b"
LINE = "#cbd5e1"
FILL = {
    1: "#dbeafe",
    2: "#bbf7d0",
    4: "#fed7aa",
    8: "#fecaca",
}
EDGE = {
    1: BLUE,
    2: GREEN,
    4: ORANGE,
    8: RED,
}

# 1-based. Zero slot unused.
A = [0, 3, 2, 1, 4, 5, 1, 2, 3]
N = 8


def lowbit(i: int) -> int:
    return i & -i


def build(a: list[int]) -> list[int]:
    n = len(a) - 1
    t = [0] * (n + 1)
    for i in range(1, n + 1):
        t[i] += a[i]
        j = i + lowbit(i)
        if j <= n:
            t[j] += t[i]
    return t


def cover(i: int) -> tuple[int, int]:
    return i - lowbit(i) + 1, i


def prefix_path(i: int) -> list[int]:
    path = []
    while i > 0:
        path.append(i)
        i -= lowbit(i)
    return path


def update_path(i: int, n: int) -> list[int]:
    path = []
    while i <= n:
        path.append(i)
        i += lowbit(i)
    return path


def box(ax, x, y, w, h, facecolor, edgecolor, text, *, fontsize=9, textcolor=SLATE, lw=1.2):
    ax.add_patch(
        patches.FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=lw,
            edgecolor=edgecolor,
            facecolor=facecolor,
            zorder=2,
        )
    )
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=textcolor,
        zorder=3,
        fontweight="medium",
    )


def main() -> None:
    t = build(A)
    qpath = prefix_path(7)
    upath = update_path(3, N)
    qsum = sum(t[i] for i in qpath)

    fig = plt.figure(figsize=(9.4, 10.6), dpi=130)
    gs = fig.add_gridspec(4, 2, height_ratios=[1.05, 2.15, 1.55, 1.55], hspace=0.42, wspace=0.18)
    fig.suptitle("Fenwick tree (Binary Indexed Tree), n = 8", fontsize=13, color=SLATE, y=0.98)

    # ----- array -----
    ax0 = fig.add_subplot(gs[0, :])
    ax0.set_xlim(0.3, 8.7)
    ax0.set_ylim(-0.55, 1.55)
    ax0.axis("off")
    ax0.set_title("The array a[1..8]. One slot, one value.", fontsize=11, loc="left", color=SLATE, pad=4)
    for i in range(1, N + 1):
        box(ax0, i - 0.4, 0.15, 0.8, 0.85, "#f8fafc", SLATE, str(A[i]), fontsize=12)
        ax0.text(i, 0.02, f"a[{i}]", ha="center", va="top", fontsize=8, color=MUTED)
    ax0.text(4.5, -0.42, "index", ha="center", fontsize=8, color=MUTED)

    # ----- coverage -----
    ax1 = fig.add_subplot(gs[1, :])
    ax1.set_xlim(0.3, 9.6)
    ax1.set_ylim(0.2, 9.0)
    ax1.axis("off")
    ax1.set_title(
        "Slot tree[i] stores the sum of a block that ends at i. Block length = i & -i.",
        fontsize=11,
        loc="left",
        color=SLATE,
        pad=4,
    )
    for x in range(1, N + 1):
        ax1.plot([x, x], [0.45, 8.55], color=LINE, lw=0.7, zorder=0)
        ax1.text(x, 0.28, str(x), ha="center", fontsize=8, color=MUTED)
    for row, i in enumerate(range(1, N + 1)):
        y = 8.2 - row * 0.95
        lo, hi = cover(i)
        span = lowbit(i)
        ax1.add_patch(
            patches.FancyBboxPatch(
                (lo - 0.42, y - 0.32),
                (hi - lo) + 0.84,
                0.64,
                boxstyle="round,pad=0.02,rounding_size=0.06",
                linewidth=1.3,
                edgecolor=EDGE[span],
                facecolor=FILL[span],
                zorder=2,
            )
        )
        ax1.text(
            (lo + hi) / 2,
            y,
            f"tree[{i}] = {t[i]}    Σ a[{lo}..{hi}]",
            ha="center",
            va="center",
            fontsize=8.5,
            color=SLATE,
            zorder=3,
        )
        ax1.text(
            9.15,
            y,
            f"i={i:04b}  lowbit={span}",
            ha="left",
            va="center",
            fontsize=7.5,
            color=MUTED,
            family="monospace",
        )

    # ----- prefix query -----
    ax2 = fig.add_subplot(gs[2, 0])
    ax2.set_xlim(0.2, 5.0)
    ax2.set_ylim(-0.3, 4.2)
    ax2.axis("off")
    ax2.set_title("Prefix sum: a[1] + … + a[7]", fontsize=11, loc="left", color=SLATE, pad=2)
    ax2.text(0.3, 3.7, "Start at i = 7. Repeat i = i − (i & −i) until i = 0.", fontsize=8, color=MUTED)
    steps = [("7", "0111", "tree[7] = 2", "covers [7..7]"), ("6", "0110", "tree[6] = 6", "covers [5..6]"), ("4", "0100", "tree[4] = 10", "covers [1..4]")]
    for k, (idx, bits, val, cov) in enumerate(steps):
        y = 2.85 - k * 0.95
        box(ax2, 0.35, y, 0.7, 0.7, FILL[lowbit(int(idx))], EDGE[lowbit(int(idx))], idx, fontsize=12)
        ax2.text(1.2, y + 0.48, f"i = {bits}₂", fontsize=8, color=MUTED, va="center", family="monospace")
        ax2.text(1.2, y + 0.18, val, fontsize=9, color=SLATE, va="center")
        ax2.text(1.2, y - 0.08, cov, fontsize=8, color=MUTED, va="center")
        if k < 2:
            ax2.annotate(
                "",
                xy=(0.7, y - 0.12),
                xytext=(0.7, y - 0.22),
                arrowprops=dict(arrowstyle="-|>", color=SLATE, lw=1.2),
            )
    ax2.text(0.35, -0.05, f"sum = 2 + 6 + 10 = {qsum}", fontsize=10, color=GREEN, fontweight="bold")

    # ----- update -----
    ax3 = fig.add_subplot(gs[2, 1])
    ax3.set_xlim(0.2, 5.0)
    ax3.set_ylim(-0.3, 4.2)
    ax3.axis("off")
    ax3.set_title("Update: add +1 at index 3", fontsize=11, loc="left", color=SLATE, pad=2)
    ax3.text(0.3, 3.7, "Start at i = 3. Repeat i = i + (i & −i) while i ≤ n.", fontsize=8, color=MUTED)
    usteps = [("3", "0011", "tree[3]", "parent 3+1=4"), ("4", "0100", "tree[4]", "parent 4+4=8"), ("8", "1000", "tree[8]", "8+8=16 > n, stop")]
    for k, (idx, bits, val, note) in enumerate(usteps):
        y = 2.85 - k * 0.95
        box(ax3, 0.35, y, 0.7, 0.7, FILL[lowbit(int(idx))], EDGE[lowbit(int(idx))], idx, fontsize=12)
        ax3.text(1.2, y + 0.48, f"i = {bits}₂", fontsize=8, color=MUTED, va="center", family="monospace")
        ax3.text(1.2, y + 0.18, f"add +1 to {val}", fontsize=9, color=SLATE, va="center")
        ax3.text(1.2, y - 0.08, note, fontsize=8, color=MUTED, va="center")
        if k < 2:
            ax3.annotate(
                "",
                xy=(0.7, y - 0.12),
                xytext=(0.7, y - 0.22),
                arrowprops=dict(arrowstyle="-|>", color=SLATE, lw=1.2),
            )
    ax3.text(0.35, -0.05, "range [L, R] = prefix(R) − prefix(L−1)", fontsize=9, color=ORANGE, fontweight="bold")

    # ----- rules -----
    ax4 = fig.add_subplot(gs[3, :])
    ax4.set_xlim(0, 10)
    ax4.set_ylim(0, 1)
    ax4.axis("off")
    rules = (
        "lowbit(i) = i & −i  (lowest set bit).    "
        "tree[i] covers [i − lowbit(i) + 1, i].    "
        "Query walks to 0. Update walks to n.    "
        "Both touch O(log n) slots."
    )
    ax4.text(5, 0.55, rules, ha="center", va="center", fontsize=8.5, color=MUTED)
    ax4.text(
        5,
        0.18,
        "blue = length 1   |   green = length 2   |   orange = length 4   |   red = length 8",
        ha="center",
        fontsize=8,
        color=MUTED,
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    buf.seek(0)
    Image.open(buf).convert("RGB").save(OUT, optimize=True)
    print(f"Wrote {OUT}")
    print("tree", t[1:])
    print("prefix(7) path", qpath, "sum", qsum)
    print("update(3) path", upath)


if __name__ == "__main__":
    main()
