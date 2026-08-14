#!/usr/bin/env python3
"""Generate closest-pair line sweep animation for the blog post."""

from __future__ import annotations

import math
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "images" / "posts" / "line-sweep"
SPAN = 2_000_001  # matches the C++ cap; used while best is still unknown


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    label: str


# Hand-picked set: closest pair is E–I at sqrt(2).
POINTS = [
    Point(1, 1, "A"),
    Point(2, 5, "B"),
    Point(3, 2, "C"),
    Point(6, 3, "I"),
    Point(5, 2, "E"),
    Point(6, 6, "D"),
    Point(7, 1, "J"),
    Point(9, 1, "F"),
    Point(11, 7, "G"),
    Point(13, 2, "H"),
]


def sq(v: int) -> int:
    return v * v


def dist2(a: Point, b: Point) -> int:
    return sq(a.x - b.x) + sq(a.y - b.y)


def simulate(points: list[Point]) -> list[dict]:
    """Mirror the C++ sweep: sort by x, track active window and best pair."""
    order = sorted(range(len(points)), key=lambda i: (points[i].x, points[i].y))
    best = math.inf
    best_pair: tuple[int, int] | None = None
    left = 0  # leftmost index in sorted order still inside the x-window
    active: list[int] = []
    frames: list[dict] = []

    for step, pi in enumerate(order):
        p = points[pi]

        evicted: list[int] = []
        while left < step and sq(p.x - points[order[left]].x) >= best:
            idx = order[left]
            if idx in active:
                active.remove(idx)
            evicted.append(idx)
            left += 1

        d = SPAN
        if best < math.inf:
            d = min(SPAN, math.ceil(math.sqrt(best) - 1e-9))
            while d < SPAN and d * d < best:
                d += 1

        candidates: list[int] = []
        for j in active:
            q = points[j]
            if abs(q.y - p.y) <= d + 1e-9:
                candidates.append(j)
                cand_dist = dist2(p, q)
                if cand_dist < best:
                    best = cand_dist
                    best_pair = (j, pi)

        active.append(pi)

        frames.append(
            {
                "step": step + 1,
                "current": pi,
                "left": left,
                "active": list(active),
                "evicted": list(evicted),
                "candidates": candidates,
                "best": best,
                "best_pair": best_pair,
                "d": d,
            }
        )

    return frames


def render_frame(
    points: list[Point],
    frame: dict,
    *,
    order: list[int],
) -> Image.Image:
    current = frame["current"]
    active = set(frame["active"])
    candidates = set(frame["candidates"])
    processed = set(order[: frame["step"]])
    evicted = set(order[: frame["left"]])

    fig, ax = plt.subplots(figsize=(8, 5), dpi=120)
    ax.set_aspect("equal")
    ax.set_xlim(-0.5, 14.5)
    ax.set_ylim(-0.5, 8.5)
    ax.grid(True, linestyle=":", alpha=0.35)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # x-window behind the sweep line (width d when d is known).
    px = points[current].x
    d = frame["d"]
    if 0 < d < 15:
        ax.axvspan(px - d, px, color="#dbeafe", alpha=0.55, zorder=0)
        py = points[current].y
        rect = patches.Rectangle(
            (px - d, py - d),
            d,
            2 * d,
            linewidth=1.5,
            edgecolor="#16a34a",
            facecolor="#bbf7d0",
            alpha=0.35,
            zorder=1,
        )
        ax.add_patch(rect)

    ax.axvline(px, color="#dc2626", linewidth=2, linestyle="-", zorder=2)

    for idx, pt in enumerate(points):
        if idx == current:
            color = "#dc2626"
            size = 90
            z = 5
        elif idx in candidates:
            color = "#16a34a"
            size = 70
            z = 4
        elif idx in active:
            color = "#2563eb"
            size = 65
            z = 3
        elif idx in processed:
            color = "#94a3b8"
            size = 55
            z = 2
        else:
            color = "#cbd5e1"
            size = 50
            z = 2

        ax.scatter(pt.x, pt.y, s=size, c=color, edgecolors="white", linewidths=0.8, zorder=z)
        ax.text(pt.x + 0.15, pt.y + 0.15, pt.label, fontsize=9, zorder=6)

    if frame["best_pair"] is not None:
        a, b = frame["best_pair"]
        pa, pb = points[a], points[b]
        ax.plot([pa.x, pb.x], [pa.y, pb.y], color="#ea580c", linewidth=2, zorder=4)
        mid_x = (pa.x + pb.x) / 2
        mid_y = (pa.y + pb.y) / 2
        ax.text(
            mid_x,
            mid_y - 0.35,
            f"d = {math.sqrt(frame['best']):.2f}",
            fontsize=9,
            color="#ea580c",
            ha="center",
            zorder=6,
        )

    title = f"Step {frame['step']}/{len(order)} — sweep at {points[current].label}"
    if d > 0:
        title += f", band width d = {d:.2f}"
    ax.set_title(title, fontsize=11, pad=10)

    legend_text = (
        "red = sweep line & current point  |  "
        "blue = active set  |  "
        "green = candidates in y-band  |  "
        "orange = best pair so far"
    )
    fig.text(0.5, 0.02, legend_text, ha="center", fontsize=8, color="#475569")

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("P", palette=Image.ADAPTIVE)


def build_gif(frames: list[Image.Image], out_path: Path, *, pause_ms: int = 900) -> None:
    durations = [pause_ms] * len(frames)
    durations[-1] = pause_ms * 3
    out_path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
    )


def build_poster(frame: Image.Image, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    frame.save(out_path, optimize=True)


def main() -> None:
    order = sorted(range(len(POINTS)), key=lambda i: (POINTS[i].x, POINTS[i].y))
    frames_data = simulate(POINTS)
    images = [render_frame(POINTS, frame, order=order) for frame in frames_data]

    gif_path = OUT_DIR / "closest-pair-sweep.gif"
    poster_path = OUT_DIR / "closest-pair-sweep-poster.png"

    build_gif(images, gif_path)
    build_poster(images[-1], poster_path)

    print(f"Wrote {gif_path} ({len(images)} frames)")
    print(f"Wrote {poster_path}")


if __name__ == "__main__":
    main()
