#!/usr/bin/env python3
"""Generate DFS / BFS / sliding-window figures for the stack-queue-deque post."""

from __future__ import annotations

from collections import deque
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "images" / "posts" / "stack-queue-deque"

RED = "#dc2626"
BLUE = "#2563eb"
BLUE_FILL = "#dbeafe"
GREEN = "#16a34a"
GREEN_FILL = "#bbf7d0"
ORANGE = "#ea580c"
ORANGE_FILL = "#fed7aa"
SLATE = "#334155"
MUTED = "#94a3b8"
GRID = "#cbd5e1"
PANEL = "#f8fafc"

# Same undirected graph for DFS and BFS (each edge is two-way).
# Recursive DFS with this adjacency order visits A, B, D, E, C, F.
LABELS = ["A", "B", "C", "D", "E", "F"]
POS = {
    "A": (0.0, 2.15),
    "B": (-1.45, 0.95),
    "C": (1.45, 0.95),
    "D": (-2.15, -0.35),
    "E": (-0.75, -0.35),
    "F": (1.45, -0.35),
}
ADJ = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B"],
    "F": ["C"],
}
EDGES = [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F")]
NODE_R = 0.28

WINDOW = [1, 3, -1, -3, 5, 3, 6, 7]
K = 3


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


def save_gif(images: list[Image.Image], path: Path, *, pause_ms: int = 2000) -> None:
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


def legend(fig: plt.Figure, text: str) -> None:
    fig.text(0.5, 0.015, text, ha="center", fontsize=8, color="#475569")


def simulate_dfs(start: str = "A") -> list[dict]:
    stack = [start]
    visited: set[str] = set()
    frames = [
        {
            "title": "Start — push A",
            "current": None,
            "stack": list(stack),
            "visited": set(),
            "fresh": {start},
            "path": [],
        }
    ]
    parent: dict[str, str | None] = {start: None}

    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        path: list[str] = []
        x: str | None = u
        while x is not None:
            path.append(x)
            x = parent.get(x)
        path.reverse()
        fresh: list[str] = []
        for v in reversed(ADJ[u]):
            if v not in visited:
                stack.append(v)
                fresh.append(v)
                parent.setdefault(v, u)
        frames.append(
            {
                "title": f"Pop {u}" + (f", push {', '.join(reversed(fresh))}" if fresh else ""),
                "current": u,
                "stack": list(stack),
                "visited": set(visited),
                "fresh": set(fresh),
                "path": path,
            }
        )
    return frames


def simulate_bfs(start: str = "A") -> list[dict]:
    q: deque[str] = deque([start])
    visited = {start}
    parent: dict[str, str | None] = {start: None}
    frames = [
        {
            "title": "Start — enqueue A",
            "current": None,
            "queue": list(q),
            "visited": set(),
            "fresh": {start},
            "path": [],
        }
    ]
    while q:
        u = q.popleft()
        path: list[str] = []
        x: str | None = u
        while x is not None:
            path.append(x)
            x = parent.get(x)
        path.reverse()
        fresh: list[str] = []
        for v in ADJ[u]:
            if v not in visited:
                visited.add(v)
                q.append(v)
                fresh.append(v)
                parent[v] = u
        frames.append(
            {
                "title": f"Dequeue {u}" + (f", enqueue {', '.join(fresh)}" if fresh else ""),
                "current": u,
                "queue": list(q),
                "visited": set(visited) | {u},
                "fresh": set(fresh),
                "path": path,
            }
        )
    return frames


def draw_directed_edge(ax, u: str, v: str, *, color: str, lw: float) -> None:
    x0, y0 = POS[u]
    x1, y1 = POS[v]
    dx, dy = x1 - x0, y1 - y0
    length = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / length, dy / length
    pad = NODE_R + 0.02
    ax.annotate(
        "",
        xy=(x1 - ux * pad, y1 - uy * pad),
        xytext=(x0 + ux * pad, y0 + uy * pad),
        arrowprops=dict(arrowstyle="<|-|>", color=color, lw=lw, mutation_scale=12),
        zorder=1,
    )


def draw_graph(ax, *, current, visited, frontier, fresh, path) -> None:
    ax.set_xlim(-3.05, 2.45)
    ax.set_ylim(-1.15, 2.85)
    ax.set_aspect("equal")
    ax.axis("off")

    path_edges = {frozenset((a, b)) for a, b in zip(path, path[1:])}

    for u, v in EDGES:
        if frozenset((u, v)) in path_edges:
            draw_directed_edge(ax, u, v, color=ORANGE, lw=2.4)
        else:
            draw_directed_edge(ax, u, v, color=GRID, lw=1.5)

    for lab in LABELS:
        x, y = POS[lab]
        if lab == current:
            fc, ec, r = "#fecaca", RED, 0.28
        elif lab in fresh:
            fc, ec, r = GREEN_FILL, GREEN, 0.26
        elif lab in frontier:
            fc, ec, r = BLUE_FILL, BLUE, 0.26
        elif lab in visited:
            fc, ec, r = "#e2e8f0", MUTED, 0.24
        else:
            fc, ec, r = "white", GRID, 0.24
        ax.add_patch(patches.Circle((x, y), r, facecolor=fc, edgecolor=ec, linewidth=1.8, zorder=3))
        ax.text(x, y, lab, ha="center", va="center", fontsize=11, color=SLATE, zorder=4, fontweight="bold")


def draw_column(ax, items: list[str], *, title: str, top_is_end: bool, current: str | None, fresh) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.15, 7.2)
    ax.axis("off")
    ax.set_title(title, fontsize=11, pad=6, color=SLATE)

    ax.add_patch(
        patches.FancyBboxPatch(
            (0.18, 0.15),
            0.64,
            6.4,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor=PANEL,
            edgecolor=GRID,
            linewidth=1.2,
        )
    )

    for i, lab in enumerate(items):
        y = 0.45 + i * 0.95
        if lab == current:
            fc, ec = "#fecaca", RED
        elif lab in fresh:
            fc, ec = GREEN_FILL, GREEN
        else:
            fc, ec = BLUE_FILL, BLUE
        ax.add_patch(
            patches.FancyBboxPatch(
                (0.28, y),
                0.44,
                0.72,
                boxstyle="round,pad=0.01,rounding_size=0.06",
                facecolor=fc,
                edgecolor=ec,
                linewidth=1.4,
                zorder=2,
            )
        )
        ax.text(0.50, y + 0.36, lab, ha="center", va="center", fontsize=12, color=SLATE, fontweight="bold", zorder=3)

    if top_is_end:
        ax.text(0.50, 6.75, "top (pop)", ha="center", va="center", fontsize=8, color=MUTED)
        ax.text(0.50, 0.02, "bottom", ha="center", va="center", fontsize=8, color=MUTED)
    else:
        ax.text(0.50, 0.02, "front (pop)", ha="center", va="center", fontsize=8, color=MUTED)
        ax.text(0.50, 6.75, "back (push)", ha="center", va="center", fontsize=8, color=MUTED)


def render_walk_frame(frame: dict, *, kind: str, step: int, total: int) -> Image.Image:
    fig, (ax_g, ax_c) = plt.subplots(
        1,
        2,
        figsize=(8.4, 4.8),
        dpi=120,
        gridspec_kw={"width_ratios": [3.2, 1.15]},
    )
    if kind == "stack":
        container = frame["stack"]
        frontier = set(container)
        draw_graph(
            ax_g,
            current=frame["current"],
            visited=frame["visited"],
            frontier=frontier,
            fresh=frame["fresh"],
            path=frame["path"],
        )
        draw_column(
            ax_c,
            container,
            title="stack",
            top_is_end=True,
            current=None,
            fresh=frame["fresh"],
        )
        fig.suptitle(f"DFS  ·  step {step}/{total}  ·  {frame['title']}", fontsize=12, color=SLATE, y=0.98)
        legend(fig, "red = current  ·  blue = still in the stack  ·  green = just pushed  ·  orange = path from the start")
    else:
        container = frame["queue"]
        frontier = set(container)
        draw_graph(
            ax_g,
            current=frame["current"],
            visited=frame["visited"],
            frontier=frontier,
            fresh=frame["fresh"],
            path=frame["path"],
        )
        draw_column(
            ax_c,
            container,
            title="queue",
            top_is_end=False,
            current=None,
            fresh=frame["fresh"],
        )
        fig.suptitle(f"BFS  ·  step {step}/{total}  ·  {frame['title']}", fontsize=12, color=SLATE, y=0.98)
        legend(fig, "red = current  ·  blue = still in the queue  ·  green = just enqueued  ·  orange = BFS tree path")

    fig.tight_layout(rect=(0.02, 0.05, 0.98, 0.93))
    return fig_to_image(fig)


def simulate_window(values: list[int], k: int) -> list[dict]:
    dq: deque[int] = deque()
    frames: list[dict] = []
    answers: list[int] = []

    frames.append(
        {
            "i": -1,
            "left": 0,
            "right": -1,
            "dq": [],
            "dropped_left": None,
            "popped": [],
            "answers": [],
            "title": f"Empty deque. Window width k = {k}.",
        }
    )

    for i, x in enumerate(values):
        dropped_left = None
        left = i - k + 1
        if dq and dq[0] < left:
            dropped_left = dq.popleft()

        popped: list[int] = []
        while dq and values[dq[-1]] <= x:
            popped.append(dq.pop())
        dq.append(i)

        ans = None
        if i >= k - 1:
            ans = values[dq[0]]
            answers.append(ans)

        frames.append(
            {
                "i": i,
                "left": max(0, left),
                "right": i,
                "dq": list(dq),
                "dropped_left": dropped_left,
                "popped": popped,
                "answers": list(answers),
                "title": _window_title(i, x, dropped_left, popped, ans, values),
            }
        )
    return frames


def _window_title(i: int, x: int, dropped_left, popped, ans, values) -> str:
    bits = [f"arrive a[{i}] = {x}"]
    if dropped_left is not None:
        bits.append(f"index {dropped_left} left the window")
    if popped:
        bits.append("pop " + ", ".join(str(values[j]) for j in popped) + " from the back")
    bits.append(f"push {x}")
    if ans is not None:
        bits.append(f"max = {ans}")
    return "; ".join(bits)


def render_window_frame(frame: dict, values: list[int], k: int, *, step: int, total: int) -> Image.Image:
    fig, axes = plt.subplots(3, 1, figsize=(8.6, 5.2), dpi=120, gridspec_kw={"height_ratios": [1.15, 1.0, 0.7]})
    ax_a, ax_d, ax_o = axes
    for ax in axes:
        ax.axis("off")

    fig.suptitle(f"Sliding window  ·  step {step}/{total}  ·  {frame['title']}", fontsize=11, color=SLATE, y=0.98)

    ax_a.set_xlim(-0.6, len(values) - 0.4)
    ax_a.set_ylim(-0.7, 1.5)
    ax_a.set_title("array", fontsize=10, loc="left", color=MUTED, pad=2)

    left, right = frame["left"], frame["right"]
    if right >= 0:
        ax_a.add_patch(
            patches.FancyBboxPatch(
                (left - 0.42, -0.35),
                (right - left) + 0.84,
                1.35,
                boxstyle="round,pad=0.01,rounding_size=0.08",
                facecolor="#eff6ff",
                edgecolor=BLUE,
                linewidth=1.5,
                zorder=0,
            )
        )

    for i, v in enumerate(values):
        if frame["i"] < 0:
            fc, ec = "white", GRID
        elif i == frame["i"]:
            fc, ec = "#fecaca", RED
        elif left <= i <= right:
            fc, ec = BLUE_FILL, BLUE
        else:
            fc, ec = "#f1f5f9", GRID
        ax_a.add_patch(
            patches.FancyBboxPatch(
                (i - 0.36, -0.12),
                0.72,
                0.9,
                boxstyle="round,pad=0.01,rounding_size=0.06",
                facecolor=fc,
                edgecolor=ec,
                linewidth=1.3,
                zorder=2,
            )
        )
        ax_a.text(i, 0.36, str(v), ha="center", va="center", fontsize=12, color=SLATE, fontweight="bold", zorder=3)
        ax_a.text(i, -0.52, str(i), ha="center", va="center", fontsize=8, color=MUTED)

    ax_d.set_xlim(-0.8, 8.2)
    ax_d.set_ylim(-0.55, 1.45)
    ax_d.set_title("deque of indices  (front holds the max)", fontsize=10, loc="left", color=MUTED, pad=2)
    ax_d.text(-0.55, 0.45, "front", ha="center", va="center", fontsize=8, color=MUTED, rotation=90)
    ax_d.text(7.9, 0.45, "back", ha="center", va="center", fontsize=8, color=MUTED, rotation=90)

    dq = frame["dq"]
    popped = set(frame["popped"] or [])
    for slot in range(6):
        x = slot * 1.15 + 0.35
        ax_d.add_patch(
            patches.FancyBboxPatch(
                (x, -0.05),
                0.95,
                1.05,
                boxstyle="round,pad=0.01,rounding_size=0.06",
                facecolor=PANEL,
                edgecolor=GRID,
                linewidth=1.0,
                zorder=1,
            )
        )
        if slot < len(dq):
            idx = dq[slot]
            fc = ORANGE_FILL if slot == 0 else GREEN_FILL
            ec = ORANGE if slot == 0 else GREEN
            ax_d.add_patch(
                patches.FancyBboxPatch(
                    (x + 0.06, 0.04),
                    0.83,
                    0.88,
                    boxstyle="round,pad=0.01,rounding_size=0.05",
                    facecolor=fc,
                    edgecolor=ec,
                    linewidth=1.4,
                    zorder=2,
                )
            )
            ax_d.text(x + 0.47, 0.62, str(values[idx]), ha="center", va="center", fontsize=12, color=SLATE, fontweight="bold")
            ax_d.text(x + 0.47, 0.22, f"i={idx}", ha="center", va="center", fontsize=8, color=MUTED)

    if frame["dropped_left"] is not None:
        ax_d.text(0.15, 1.25, f"pop_front index {frame['dropped_left']}", fontsize=8, color=RED)
    if popped:
        ax_d.text(3.4, 1.25, "pop_back smaller values", fontsize=8, color=ORANGE)

    ax_o.set_xlim(-0.5, 7.5)
    ax_o.set_ylim(-0.4, 1.15)
    ax_o.set_title("window maxima so far", fontsize=10, loc="left", color=MUTED, pad=2)
    answers = frame["answers"]
    for i, ans in enumerate(answers):
        ax_o.add_patch(
            patches.FancyBboxPatch(
                (i * 1.05, 0.05),
                0.9,
                0.75,
                boxstyle="round,pad=0.01,rounding_size=0.05",
                facecolor=ORANGE_FILL,
                edgecolor=ORANGE,
                linewidth=1.2,
            )
        )
        ax_o.text(i * 1.05 + 0.45, 0.42, str(ans), ha="center", va="center", fontsize=12, color=SLATE, fontweight="bold")
    if not answers:
        ax_o.text(0, 0.4, "window not full yet", fontsize=10, color=MUTED)

    legend(fig, "red = arriving cell  ·  blue = current window  ·  orange front = current maximum")
    fig.tight_layout(rect=(0.02, 0.05, 0.98, 0.93))
    return fig_to_image(fig)


# Directed 0/1 graph. Cheap path S-A-T costs 0. Direct S-T costs 1.
# Hop-count BFS marks T at cost 1 and never finds the cheap path.
ZERO_POS = {
    "S": (-1.85, 1.05),
    "A": (0.05, 2.15),
    "B": (0.05, -0.15),
    "T": (1.95, 1.05),
}
ZERO_ADJ = {
    "S": [("A", 0), ("T", 1), ("B", 1)],
    "A": [("T", 0)],
    "B": [("T", 0)],
    "T": [],
}
ZERO_EDGES = [("S", "A", 0), ("A", "T", 0), ("S", "T", 1), ("S", "B", 1), ("B", "T", 0)]
INF = 99


def simulate_01_bfs(start: str = "S") -> list[dict]:
    dist = {n: INF for n in ZERO_POS}
    dist[start] = 0
    dq: deque[str] = deque([start])
    frames = [
        {
            "title": "Start at S, cost 0. Deque holds S.",
            "current": None,
            "deque": list(dq),
            "dist": dict(dist),
            "fresh": {start},
            "improved": set(),
            "used": None,
        }
    ]

    while dq:
        u = dq.popleft()
        improved: set[str] = set()
        fresh: list[str] = []
        fronts: list[str] = []
        backs: list[str] = []
        used = None
        for v, w in ZERO_ADJ[u]:
            cand = dist[u] + w
            if cand < dist[v]:
                dist[v] = cand
                improved.add(v)
                used = (u, v, w)
                if w == 0:
                    dq.appendleft(v)
                    fronts.append(v)
                else:
                    dq.append(v)
                    backs.append(v)
                fresh.append(v)
        frames.append(
            {
                "title": _zero_title(u, dist, fronts, backs),
                "current": u,
                "deque": list(dq),
                "dist": dict(dist),
                "fresh": set(fresh),
                "improved": improved,
                "used": used,
            }
        )
    return frames


def _zero_title(u: str, dist: dict, fronts: list[str], backs: list[str]) -> str:
    if not fronts and not backs:
        return f"Pop {u}. No cheaper neighbour."
    bits = [f"Pop {u}"]
    if fronts:
        bits.append(
            "front: " + ", ".join(f"{v} costs {dist[v]}" for v in fronts)
        )
    if backs:
        bits.append(
            "back: " + ", ".join(f"{v} costs {dist[v]}" for v in backs)
        )
    return ". ".join(bits) + "."


def _edge_points(u: str, v: str, r: float = 0.32):
    x0, y0 = ZERO_POS[u]
    x1, y1 = ZERO_POS[v]
    dx, dy = x1 - x0, y1 - y0
    length = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / length, dy / length
    # Bend the direct S-T chord down so it does not sit on A.
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    if {u, v} == {"S", "T"}:
        mx, my = mx, my - 0.08
    return (x0 + ux * r, y0 + uy * r), (x1 - ux * r, y1 - uy * r), (mx, my)


def render_01_frame(frame: dict, *, step: int, total: int) -> Image.Image:
    fig, (ax_g, ax_c) = plt.subplots(
        1,
        2,
        figsize=(8.6, 4.9),
        dpi=120,
        gridspec_kw={"width_ratios": [3.3, 1.15]},
    )
    ax_g.set_xlim(-2.55, 2.65)
    ax_g.set_ylim(-0.95, 2.85)
    ax_g.set_aspect("equal")
    ax_g.axis("off")

    used = frame["used"]
    cheap = {("S", "A"), ("A", "T")}
    for u, v, w in ZERO_EDGES:
        p0, p1, mid = _edge_points(u, v)
        if used == (u, v, w):
            color, lw = ORANGE, 2.6
        elif (u, v) in cheap and frame["dist"].get("T", INF) == 0:
            color, lw = GREEN, 2.2
        elif w == 0:
            color, lw = "#86efac", 1.6
        else:
            color, lw = "#fdba74", 1.6
        ax_g.annotate(
            "",
            xy=p1,
            xytext=p0,
            arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=12),
            zorder=1,
        )
        ax_g.text(
            mid[0],
            mid[1] + (0.16 if {u, v} != {"S", "T"} else -0.22),
            str(w),
            ha="center",
            va="center",
            fontsize=10,
            color=SLATE,
            fontweight="bold",
            zorder=5,
        )

    for lab, (x, y) in ZERO_POS.items():
        d = frame["dist"][lab]
        if lab == frame["current"]:
            fc, ec, r = "#fecaca", RED, 0.30
        elif lab in frame["improved"]:
            fc, ec, r = GREEN_FILL, GREEN, 0.28
        elif lab in frame["deque"]:
            fc, ec, r = BLUE_FILL, BLUE, 0.28
        elif d < INF:
            fc, ec, r = "#e2e8f0", MUTED, 0.26
        else:
            fc, ec, r = "white", GRID, 0.26
        ax_g.add_patch(patches.Circle((x, y), r, facecolor=fc, edgecolor=ec, linewidth=1.8, zorder=3))
        ax_g.text(x, y + 0.04, lab, ha="center", va="center", fontsize=12, color=SLATE, fontweight="bold", zorder=4)
        ax_g.text(
            x,
            y - 0.52,
            "∞" if d >= INF else f"cost {d}",
            ha="center",
            va="center",
            fontsize=8,
            color=MUTED,
            zorder=4,
        )

    draw_column(
        ax_c,
        frame["deque"],
        title="deque",
        top_is_end=False,
        current=None,
        fresh=frame["fresh"],
    )
    fig.suptitle(f"0-1 BFS  ·  step {step}/{total}  ·  {frame['title']}", fontsize=11, color=SLATE, y=0.98)
    legend(fig, "green edge = weight 0  ·  orange edge = the relax this step  ·  1-edges are pale orange")
    fig.tight_layout(rect=(0.02, 0.05, 0.98, 0.93))
    return fig_to_image(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    dfs_frames = simulate_dfs()
    bfs_frames = simulate_bfs()
    win_frames = simulate_window(WINDOW, K)
    zero_frames = simulate_01_bfs()

    dfs_imgs = [render_walk_frame(f, kind="stack", step=i + 1, total=len(dfs_frames)) for i, f in enumerate(dfs_frames)]
    bfs_imgs = [render_walk_frame(f, kind="queue", step=i + 1, total=len(bfs_frames)) for i, f in enumerate(bfs_frames)]
    win_imgs = [render_window_frame(f, WINDOW, K, step=i + 1, total=len(win_frames)) for i, f in enumerate(win_frames)]
    zero_imgs = [render_01_frame(f, step=i + 1, total=len(zero_frames)) for i, f in enumerate(zero_frames)]

    dfs_gif = OUT_DIR / "dfs-stack.gif"
    bfs_gif = OUT_DIR / "bfs-queue.gif"
    win_gif = OUT_DIR / "sliding-window-deque.gif"
    zero_gif = OUT_DIR / "zero-one-bfs.gif"

    save_gif(dfs_imgs, dfs_gif)
    save_gif(bfs_imgs, bfs_gif)
    save_gif(win_imgs, win_gif)
    save_gif(zero_imgs, zero_gif)

    print(f"Wrote {dfs_gif} ({len(dfs_imgs)} frames)")
    print(f"Wrote {bfs_gif} ({len(bfs_imgs)} frames)")
    print(f"Wrote {win_gif} ({len(win_imgs)} frames)")
    print(f"Wrote {zero_gif} ({len(zero_imgs)} frames)")


if __name__ == "__main__":
    main()
