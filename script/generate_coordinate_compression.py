#!/usr/bin/env python3
"""Generate coordinate-compression figures for the blog post."""

from __future__ import annotations

from collections import deque
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "images" / "posts" / "coordinate-compression"

RED = "#dc2626"
BLUE = "#2563eb"
GREEN = "#16a34a"
GREEN_FILL = "#bbf7d0"
ORANGE = "#ea580c"
SLATE = "#334155"
MUTED = "#94a3b8"
GRID = "#cbd5e1"
WALL = "#1e293b"
EMPTY = "#f8fafc"
PATH = "#ea580c"
KEEP = "#2563eb"
COLLAPSE = "#16a34a"

# Shared example: four x-coordinates, two half-open intervals.
XS = [2, 7, 20, 23]
INTERVALS = [(2, 7), (20, 23)]  # lengths 5 and 3
RANKS = {x: i + 1 for i, x in enumerate(XS)}

MAZE = [
    "###############",
    "#S            #",
    "#             #",
    "#      ###    #",
    "#      # #    #",
    "#      # #    #",
    "#        #    #",
    "#      ###    #",
    "#            E#",
    "#             #",
    "###############",
]


def fig_to_image(fig: plt.Figure) -> Image.Image:
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGB")


def pad_to_same_size(images: list[Image.Image]) -> list[Image.Image]:
    w = max(im.size[0] for im in images)
    h = max(im.size[1] for im in images)
    out: list[Image.Image] = []
    for im in images:
        canvas = Image.new("RGB", (w, h), "white")
        canvas.paste(im, ((w - im.size[0]) // 2, (h - im.size[1]) // 2))
        out.append(canvas)
    return out


def save_gif(images: list[Image.Image], path: Path, *, pause_ms: int = 900) -> None:
    frames = pad_to_same_size(images)
    durations = [pause_ms] * len(frames)
    durations[0] = pause_ms * 2
    durations[-1] = pause_ms * 3
    path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
    )


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def legend(fig: plt.Figure, text: str) -> None:
    fig.text(0.5, 0.02, text, ha="center", fontsize=8, color="#475569")


# ---------------------------------------------------------------------------
# Rank compression: empty space folds away
# ---------------------------------------------------------------------------


def _axis(ax, y: float, x0: float, x1: float) -> None:
    ax.plot([x0, x1], [y, y], color=SLATE, linewidth=1.4, zorder=1)
    step = 1 if x1 - x0 <= 8 else 5
    t = int(x0)
    while t <= x1:
        ax.plot([t, t], [y - 0.06, y + 0.06], color=GRID, linewidth=1, zorder=1)
        t += step


def render_rank_frames() -> list[Image.Image]:
    images: list[Image.Image] = []
    rank_xs = list(RANKS.values())

    def draw(title: str, *, n_arrows: int = 0, gaps: bool = False, boxes: bool = False, bottom: bool = False):
        fig, ax = plt.subplots(figsize=(8, 4.0), dpi=120)
        ax.set_xlim(-1.0, 25.0)
        ax.set_ylim(-1.7, 2.6)
        ax.axis("off")
        ax.set_title(title, fontsize=11, pad=10)

        _axis(ax, 1.55, 0, 24)
        ax.text(-0.8, 1.55, "x", ha="right", va="center", fontsize=9, color=SLATE)
        for x in XS:
            ax.scatter([x], [1.55], s=90, c=BLUE, edgecolors="white", linewidths=0.8, zorder=3)
            ax.text(x, 1.88, str(x), ha="center", fontsize=10, color=SLATE)

        if gaps:
            for a, b in zip(XS, XS[1:]):
                ax.annotate(
                    "",
                    xy=(b - 0.2, 1.12),
                    xytext=(a + 0.2, 1.12),
                    arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.2),
                )
                ax.text((a + b) / 2, 0.82, f"gap {b - a}", ha="center", fontsize=8, color=MUTED)

        rank_pos = [3 + 6 * i for i in range(len(rank_xs))]  # spread across the same width
        if bottom:
            _axis(ax, 0.05, 1, 23)
            ax.text(-0.8, 0.05, "rank", ha="right", va="center", fontsize=9, color=SLATE)
            for r, px in zip(rank_xs, rank_pos):
                ax.scatter([px], [0.05], s=90, c=ORANGE, edgecolors="white", linewidths=0.8, zorder=3)
                ax.text(px, -0.32, str(r), ha="center", fontsize=10, color=ORANGE)

        for i, (x, r, px) in enumerate(zip(XS, rank_xs, rank_pos)):
            if i >= n_arrows:
                break
            ax.annotate(
                "",
                xy=(px, 0.18),
                xytext=(x, 1.42),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.5, connectionstyle="arc3,rad=0.04"),
                zorder=2,
            )
            ax.text((x + px) / 2, 0.85, f"{x}→{r}", fontsize=8, color=BLUE)

        if boxes:
            for r, px in zip(rank_xs, rank_pos):
                ax.add_patch(
                    patches.FancyBboxPatch(
                        (px - 0.7, -1.25),
                        1.4,
                        0.5,
                        boxstyle="round,pad=0.02,rounding_size=0.08",
                        linewidth=1.2,
                        edgecolor=BLUE,
                        facecolor="#dbeafe",
                        zorder=3,
                    )
                )
                ax.text(px, -1.0, f"[{r}]", ha="center", va="center", fontsize=8, color=BLUE)

        legend(
            fig,
            "blue = original x  |  orange = rank  |  the arrows keep order and throw away distance",
        )
        return fig_to_image(fig)

    images.append(draw("Four positions. The line is mostly empty.", gaps=True))
    images.append(draw("We only need the values that appear.", bottom=True))
    for n in range(1, 5):
        images.append(draw(f"Map each x to its rank. {n}/4", n_arrows=n, bottom=True))
    images.append(
        draw(
            "Ranks 1..4. An array of length 4 is enough.",
            n_arrows=4,
            bottom=True,
            boxes=True,
        )
    )
    return images


# ---------------------------------------------------------------------------
# Coverage: the fold gives the wrong length unless edges keep their width
# ---------------------------------------------------------------------------


def _interval_strip(ax, xs, intervals, *, xlim, title, weights=None, wrong=False, total=None):
    ax.set_xlim(*xlim)
    ax.set_ylim(-1.8, 2.0)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_xlabel("x")
    ax.axhline(0, color=SLATE, linewidth=1.4, zorder=1)
    ax.set_title(title, fontsize=11, pad=10)

    for x in xs:
        ax.scatter([x], [0], s=70, c=BLUE, edgecolors="white", linewidths=0.8, zorder=4)
        ax.text(x, 0.32, str(int(round(x))), ha="center", fontsize=9, color=SLATE)

    for (lo, hi), y in zip(intervals, (0.85, 1.25)):
        ax.add_patch(
            patches.Rectangle(
                (lo, -0.18),
                hi - lo,
                0.36,
                facecolor="#fdba74",
                edgecolor=ORANGE,
                linewidth=1.3,
                alpha=0.9,
                zorder=3,
            )
        )
        label = f"[{int(round(lo))}, {int(round(hi))})"
        if weights is not None:
            w = hi - lo if not isinstance(weights, dict) else weights[(lo, hi)]
            label += f"  width {w:g}"
        ax.text((lo + hi) / 2, y, label, ha="center", fontsize=8, color=ORANGE)

    if total is not None:
        color = RED if wrong else GREEN
        prefix = "if ranks were metres: " if wrong else "true covered length: "
        ax.text(
            (xlim[0] + xlim[1]) / 2,
            -1.15,
            f"{prefix}{total}",
            ha="center",
            fontsize=11,
            color=color,
            fontweight="bold",
        )


def render_coverage_frames() -> list[Image.Image]:
    images: list[Image.Image] = []
    true_len = sum(b - a for a, b in INTERVALS)

    fig, ax = plt.subplots(figsize=(8, 3.6), dpi=120)
    _interval_strip(
        ax,
        XS,
        INTERVALS,
        xlim=(-0.5, 24.5),
        title="Two intervals. Covered length = 5 + 3 = 8.",
        weights=True,
        total=true_len,
    )
    legend(fig, "orange = covered  |  the white gap between 7 and 20 is not")
    images.append(fig_to_image(fig))

    # Fold endpoints, taking intervals with them
    for t in (0.35, 0.7, 1.0):
        xs = [s + t * (RANKS[s] - s) for s in XS]
        ivals = [
            (a + t * (RANKS[a] - a), b + t * (RANKS[b] - b)) for a, b in INTERVALS
        ]
        xlim_r = 24.5 + t * (5.5 - 24.5)
        fig, ax = plt.subplots(figsize=(8, 3.6), dpi=120)
        _interval_strip(
            ax,
            xs,
            ivals,
            xlim=(-0.5, xlim_r),
            title="The same fold. The intervals shrink with the gaps.",
        )
        legend(fig, "ranking does not preserve length")
        images.append(fig_to_image(fig))

    folded = [(RANKS[a], RANKS[b]) for a, b in INTERVALS]
    fig, ax = plt.subplots(figsize=(8, 3.6), dpi=120)
    _interval_strip(
        ax,
        list(RANKS.values()),
        folded,
        xlim=(-0.5, 5.5),
        title="Counting compressed cells as length 1 each is wrong.",
        wrong=True,
        total=sum(b - a for a, b in folded),
    )
    legend(fig, "red = the number you get if you throw the gaps away")
    images.append(fig_to_image(fig))

    # Recover with edge weights
    fig, ax = plt.subplots(figsize=(8, 3.6), dpi=120)
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-1.8, 2.2)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_xlabel("compressed index")
    ax.axhline(0, color=SLATE, linewidth=1.4, zorder=1)
    ax.set_title("Keep the original gap as the edge weight.", fontsize=11, pad=10)
    rank_list = list(RANKS.values())
    for r, x in zip(rank_list, XS):
        ax.scatter([r], [0], s=70, c=BLUE, edgecolors="white", linewidths=0.8, zorder=4)
        ax.text(r, 0.32, str(r), ha="center", fontsize=9, color=SLATE)
        ax.text(r, -0.55, f"x={x}", ha="center", fontsize=8, color=ORANGE)
    for a, b in zip(XS, XS[1:]):
        ra, rb = RANKS[a], RANKS[b]
        ax.annotate(
            "",
            xy=(rb - 0.12, 0.9),
            xytext=(ra + 0.12, 0.9),
            arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.4),
        )
        ax.text((ra + rb) / 2, 1.15, f"w = {b - a}", ha="center", fontsize=9, color=GREEN)
    ax.text(
        2.5,
        -1.25,
        "covered = w(1→2) + w(3→4) = 5 + 3 = 8",
        ha="center",
        fontsize=11,
        color=GREEN,
        fontweight="bold",
    )
    legend(fig, "green = xs[i+1] − xs[i]  |  orange = original coordinate stored at this rank")
    images.append(fig_to_image(fig))
    return images


# ---------------------------------------------------------------------------
# Maze: identical rows and columns collapse; a path maps back
# ---------------------------------------------------------------------------


def maze_cells(maze: list[str]) -> tuple[list[list[str]], tuple[int, int], tuple[int, int]]:
    grid = [list(row) for row in maze]
    start = end = None
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == "S":
                start = (x, y)
                row[x] = "."
            elif ch == "E":
                end = (x, y)
                row[x] = "."
            elif ch == " ":
                row[x] = "."
    assert start is not None and end is not None
    return grid, start, end


def row_keys(grid: list[list[str]]) -> list[tuple[str, ...]]:
    return [tuple(row) for row in grid]


def col_keys(grid: list[list[str]]) -> list[tuple[str, ...]]:
    w = len(grid[0])
    return [tuple(grid[y][x] for y in range(len(grid))) for x in range(w)]


def kept_indices(keys: list[tuple[str, ...]]) -> list[int]:
    keep = [0]
    for i in range(1, len(keys)):
        if keys[i] != keys[i - 1]:
            keep.append(i)
    return keep


def runs_of(keys: list[tuple[str, ...]]) -> list[tuple[int, int]]:
    """Inclusive runs (start, end) of identical consecutive keys, length > 1 only."""
    out = []
    start = 0
    for i in range(1, len(keys) + 1):
        if i == len(keys) or keys[i] != keys[start]:
            if i - start > 1:
                out.append((start, i - 1))
            start = i
    return out


def shortest_path(grid: list[list[str]], start: tuple[int, int], end: tuple[int, int]):
    w, h = len(grid[0]), len(grid)
    prev: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
    q = deque([start])
    while q:
        x, y = q.popleft()
        if (x, y) == end:
            break
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] != "#" and (nx, ny) not in prev:
                prev[(nx, ny)] = (x, y)
                q.append((nx, ny))
    path = []
    cur: tuple[int, int] | None = end
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    path.reverse()
    return path


def draw_maze(
    ax,
    grid: list[list[str]],
    *,
    start,
    end,
    title: str,
    row_bands=None,
    col_bands=None,
    overlay_spans=None,
    cell_colors=None,
    path=None,
    highlight_keep_rows=None,
    highlight_keep_cols=None,
    scan_row=None,
    scan_col=None,
):
    h, w = len(grid), len(grid[0])
    ax.set_xlim(-0.5, w - 0.5)
    ax.set_ylim(h - 0.5, -0.5)
    ax.set_aspect("equal")
    ax.set_xticks(range(w))
    ax.set_yticks(range(h))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(length=0)
    ax.set_title(title, fontsize=11, pad=8)
    ax.grid(True, which="major", color=GRID, linewidth=0.4, linestyle=":")

    for y in range(h):
        for x in range(w):
            if grid[y][x] == "#":
                color = WALL
            elif cell_colors and (x, y) in cell_colors:
                color = cell_colors[(x, y)]
            else:
                color = EMPTY
            ax.add_patch(
                patches.Rectangle(
                    (x - 0.5, y - 0.5),
                    1,
                    1,
                    facecolor=color,
                    edgecolor="none",
                    zorder=1,
                )
            )

    if row_bands:
        for y0, y1, color in row_bands:
            ax.add_patch(
                patches.Rectangle(
                    (-0.5, y0 - 0.5),
                    w,
                    (y1 - y0 + 1),
                    facecolor=color,
                    edgecolor="none",
                    alpha=0.28,
                    zorder=2,
                )
            )
    if col_bands:
        for x0, x1, color in col_bands:
            ax.add_patch(
                patches.Rectangle(
                    (x0 - 0.5, -0.5),
                    (x1 - x0 + 1),
                    h,
                    facecolor=color,
                    edgecolor="none",
                    alpha=0.28,
                    zorder=2,
                )
            )

    if overlay_spans:
        for x0, x1, y0, y1, color in overlay_spans:
            ax.add_patch(
                patches.Rectangle(
                    (x0 - 0.5, y0 - 0.5),
                    (x1 - x0 + 1),
                    (y1 - y0 + 1),
                    facecolor=color,
                    edgecolor=BLUE,
                    linewidth=1.1,
                    alpha=0.9,
                    zorder=3,
                )
            )

    if highlight_keep_rows is not None:
        for y in highlight_keep_rows:
            ax.axhline(y, color=KEEP, linewidth=1.6, alpha=0.8, zorder=4)
    if highlight_keep_cols is not None:
        for x in highlight_keep_cols:
            ax.axvline(x, color=KEEP, linewidth=1.6, alpha=0.8, zorder=4)

    if scan_row is not None:
        ax.axhline(scan_row, color=RED, linewidth=2.2, zorder=5)
    if scan_col is not None:
        ax.axvline(scan_col, color=RED, linewidth=2.2, zorder=5)

    if path:
        px = [p[0] for p in path]
        py = [p[1] for p in path]
        ax.plot(px, py, color=PATH, linewidth=2.4, zorder=6)
        ax.scatter(px, py, s=18, c=PATH, zorder=7)

    ax.scatter(*start, s=55, c=GREEN, edgecolors="white", linewidths=0.7, zorder=8)
    ax.scatter(*end, s=55, c=RED, edgecolors="white", linewidths=0.7, zorder=8)
    ax.text(start[0] + 0.15, start[1] - 0.35, "S", fontsize=8, color=GREEN, zorder=9)
    ax.text(end[0] + 0.15, end[1] - 0.35, "E", fontsize=8, color=RED, zorder=9)


def compress_grid(grid, keep_r, keep_c):
    return [[grid[y][x] for x in keep_c] for y in keep_r]


def map_path_to_compressed(path, keep_r, keep_c):
    def rank_on(keep, v):
        # largest kept index <= v
        out = 0
        for i, k in enumerate(keep):
            if k <= v:
                out = i
        return out

    mapped = []
    for x, y in path:
        mapped.append((rank_on(keep_c, x), rank_on(keep_r, y)))
    # collapse consecutive duplicates
    compact = [mapped[0]]
    for p in mapped[1:]:
        if p != compact[-1]:
            compact.append(p)
    return compact


REGION_PALETTE = ["#bfdbfe", "#bbf7d0", "#fde68a", "#fbcfe8", "#ddd6fe", "#a5f3fc"]


def overlay_regions(grid, keep_r, keep_c):
    """Map each empty compressed cell to a colour used on both mazes."""
    h, w = len(grid), len(grid[0])
    row_bounds = keep_r + [h]
    col_bounds = keep_c + [w]
    spans = []
    colors = {}
    k = 0
    for i, y0 in enumerate(keep_r):
        y1 = row_bounds[i + 1] - 1
        for j, x0 in enumerate(keep_c):
            x1 = col_bounds[j + 1] - 1
            if grid[y0][x0] == "#":
                continue
            color = REGION_PALETTE[k % len(REGION_PALETTE)]
            k += 1
            spans.append((x0, x1, y0, y1, color))
            colors[(j, i)] = color
    return spans, colors


def render_maze_frames() -> tuple[list[Image.Image], Image.Image]:
    grid, start, end = maze_cells(MAZE)
    path = shortest_path(grid, start, end)
    rkeys, ckeys = row_keys(grid), col_keys(grid)
    keep_r, keep_c = kept_indices(rkeys), kept_indices(ckeys)
    row_runs = runs_of(rkeys)
    col_runs = runs_of(ckeys)
    compressed = compress_grid(grid, keep_r, keep_c)

    def rank_keep(keep, v):
        out = 0
        for i, k in enumerate(keep):
            if k <= v:
                out = i
        return out

    c_start = (rank_keep(keep_c, start[0]), rank_keep(keep_r, start[1]))
    c_end = (rank_keep(keep_c, end[0]), rank_keep(keep_r, end[1]))
    c_path = map_path_to_compressed(path, keep_r, keep_c)
    spans, cell_colors = overlay_regions(grid, keep_r, keep_c)
    images: list[Image.Image] = []

    def one(title, **kwargs):
        fig, ax = plt.subplots(figsize=(8, 5.2), dpi=120)
        draw_maze(ax, grid, start=start, end=end, title=title, **kwargs)
        legend(
            fig,
            "green = start  |  red = end  |  dark = wall  |  bands = identical rows/cols that will fold",
        )
        return fig_to_image(fig)

    images.append(one("A maze whose empty rooms are huge. BFS would visit every cell."))

    images.append(
        one(
            "Identical consecutive rows. Each coloured band is one compressed row.",
            row_bands=[(a, b, COLLAPSE) for a, b in row_runs],
        )
    )

    images.append(
        one(
            "Keep a row only when it differs from the one above.",
            highlight_keep_rows=keep_r,
            row_bands=[(a, b, COLLAPSE) for a, b in row_runs],
        )
    )

    images.append(
        one(
            "Identical consecutive columns. Each band is one compressed column.",
            col_bands=[(a, b, KEEP) for a, b in col_runs],
        )
    )

    images.append(
        one(
            "Keep a column only when it differs from the one to its left.",
            highlight_keep_cols=keep_c,
            col_bands=[(a, b, KEEP) for a, b in col_runs],
        )
    )

    images.append(
        one(
            "Matching colours: each region on the left is one cell on the right.",
            overlay_spans=spans,
        )
    )

    fig, axes = plt.subplots(1, 2, figsize=(9.2, 5.0), dpi=120)
    draw_maze(
        axes[0],
        grid,
        start=start,
        end=end,
        title="Original, grouped",
        overlay_spans=spans,
        path=path,
    )
    draw_maze(
        axes[1],
        compressed,
        start=c_start,
        end=c_end,
        title=f"Compressed {len(keep_c)}×{len(keep_r)}",
        cell_colors=cell_colors,
        path=c_path,
    )
    legend(
        fig,
        "same colour = same cell  |  orange = shortest path  |  one step on the right can cover many cells on the left",
    )
    side = fig_to_image(fig)
    images.append(side)

    fig, axes = plt.subplots(1, 2, figsize=(9.2, 5.0), dpi=120)
    draw_maze(
        axes[0],
        grid,
        start=start,
        end=end,
        title="Original",
        overlay_spans=spans,
    )
    draw_maze(
        axes[1],
        compressed,
        start=c_start,
        end=c_end,
        title="Compressed",
        cell_colors=cell_colors,
    )
    fig.suptitle("Coordinate compression", fontsize=13, y=0.98, color=SLATE)
    legend(
        fig,
        "each coloured region on the left is a single cell of the same colour on the right",
    )
    poster = fig_to_image(fig)
    return images, poster


# ---------------------------------------------------------------------------
# Why extra splits: the cell beside a gap is not like the cell along the wall
# ---------------------------------------------------------------------------


def render_split_neighbors() -> Image.Image:
    # Vertical wall in column 4 with a one-cell gap at row 3.
    # Two empty cells in column 5: beside the wall vs beside the opening.
    raw = [
        ".........",
        "....#....",
        "....#....",
        ".........",
        "....#....",
        "....#....",
        ".........",
    ]
    grid = [list(row) for row in raw]
    wall_cell = (5, 2)  # left neighbour is the wall
    gap_cell = (5, 3)  # left neighbour is the opening
    gap_row = 3

    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.8), dpi=120)

    def paint(ax, title, focus, through_gap: bool):
        h, w = len(grid), len(grid[0])
        ax.set_xlim(-0.7, w - 0.3)
        ax.set_ylim(h - 0.3, -0.7)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title, fontsize=11, pad=8)
        # same-column band
        ax.add_patch(
            patches.Rectangle((4.5, -0.5), 1, h, facecolor="#dbeafe", edgecolor="none", zorder=0)
        )
        # keep c-1, c, c+1
        for y, lab in ((gap_row - 1, "c−1"), (gap_row, "c"), (gap_row + 1, "c+1")):
            ax.add_patch(
                patches.Rectangle(
                    (-0.5, y - 0.5),
                    w,
                    1,
                    facecolor="#fef9c3",
                    edgecolor="none",
                    alpha=0.55,
                    zorder=0,
                )
            )
            ax.text(-0.15, y, lab, ha="right", va="center", fontsize=8, color=ORANGE)
        for y in range(h):
            for x in range(w):
                color = WALL if grid[y][x] == "#" else EMPTY
                ax.add_patch(
                    patches.Rectangle(
                        (x - 0.5, y - 0.5),
                        1,
                        1,
                        facecolor=color,
                        edgecolor=GRID,
                        linewidth=0.6,
                        zorder=1,
                    )
                )
        fx, fy = focus
        ax.scatter([fx], [fy], s=130, c=RED, edgecolors="white", zorder=5)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = fx + dx, fy + dy
            if not (0 <= nx < w and 0 <= ny < h):
                continue
            blocked = grid[ny][nx] == "#"
            col = MUTED if blocked else GREEN
            ax.annotate(
                "",
                xy=(nx, ny),
                xytext=(fx, fy),
                arrowprops=dict(
                    arrowstyle="-|>" if not blocked else "-",
                    color=col,
                    lw=1.8,
                ),
                zorder=4,
            )
        note = "can step through the gap" if through_gap else "the wall blocks the left step"
        ax.text(4, 6.45, note, ha="center", fontsize=8, color=GREEN if through_gap else MUTED)

    paint(axes[0], "Same column, beside the wall", wall_cell, False)
    paint(axes[1], "Same column, beside the opening", gap_cell, True)
    fig.suptitle("Do not merge rows around a change. Keep c−1, c, and c+1.", fontsize=12, color=SLATE)
    legend(fig, "blue band = one column  |  yellow rows = the three splits  |  green arrow = a legal step")
    return fig_to_image(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rank = render_rank_frames()
    save_gif(rank, OUT_DIR / "rank-fold.gif", pause_ms=750)

    cover = render_coverage_frames()
    save_gif(cover, OUT_DIR / "coverage-weights.gif", pause_ms=900)

    maze_frames, poster = render_maze_frames()
    save_gif(maze_frames, OUT_DIR / "maze-compress.gif", pause_ms=1100)
    save_png(poster, OUT_DIR / "coordinate-compression-poster.png")

    split = render_split_neighbors()
    save_png(split, OUT_DIR / "split-neighbors.png")

    print(f"Wrote {len(rank)} rank frames, {len(cover)} coverage frames, {len(maze_frames)} maze frames")
    print(f"Output: {OUT_DIR}")


if __name__ == "__main__":
    main()
