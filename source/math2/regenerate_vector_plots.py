"""Regenerate the Day 2 Matplotlib figures as PDF and SVG assets.

Colours come from source/palette.py, shared with the slides.  The figure
sizes and type sizes are chosen for the final Beamer placements, so labels
remain readable after the vector art is scaled on a slide.
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from palette import SLIDE_BLUE, SLIDE_GRAY  # noqa: E402


OUTPUT_DIR = Path(__file__).resolve().parent

PLOT_STEMS = ("open-balls",)


plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 16,
        "mathtext.fontset": "cm",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "path",
    }
)


def save_vector_pair(fig: plt.Figure, stem: str) -> None:
    for suffix in ("pdf", "svg"):
        fig.savefig(
            OUTPUT_DIR / f"{stem}.{suffix}",
            bbox_inches="tight",
            pad_inches=0.035,
            facecolor="white",
        )
    svg_path = OUTPUT_DIR / f"{stem}.svg"
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


def make_open_balls_plot() -> None:
    """The open ball of radius epsilon in one, two and three dimensions.

    The excluded boundary is drawn consistently: hollow endpoints on the
    line, a dashed circle in the plane, a translucent shell in space.
    """
    eps = 1.0
    fig = plt.figure(figsize=(8.0, 2.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.5, 1.05, 1.35], wspace=0.10)

    # --- L = 1: an interval ------------------------------------------------
    ax = fig.add_subplot(gs[0, 0])
    ax.annotate(
        "",
        xy=(2.35, 0), xytext=(-2.35, 0),
        arrowprops={"arrowstyle": "-|>", "color": SLIDE_GRAY, "linewidth": 1.1},
    )
    ax.plot([-eps, eps], [0, 0], color=SLIDE_BLUE, linewidth=2.6,
            solid_capstyle="butt", zorder=2)
    ax.plot([-eps, eps], [0, 0], "o", markersize=7, zorder=3,
            markerfacecolor="white", markeredgecolor=SLIDE_BLUE,
            markeredgewidth=1.8, linestyle="none")
    ax.plot([0], [0], "o", markersize=6, color=SLIDE_BLUE, zorder=4)
    for x, label in ((-eps, r"$a-\varepsilon$"), (0, r"$a$"),
                     (eps, r"$a+\varepsilon$")):
        ax.text(x, -0.42, label, ha="center", va="top", fontsize=14,
                color=SLIDE_BLUE if x == 0 else "black")
    ax.set_xlim(-2.45, 2.45)
    ax.set_ylim(-1.35, 1.0)
    ax.set_title(r"$L=1$: an interval", fontsize=15, color=SLIDE_GRAY, pad=4)
    ax.axis("off")

    # --- L = 2: a disc -----------------------------------------------------
    ax = fig.add_subplot(gs[0, 1])
    theta = np.linspace(0, 2 * np.pi, 200)
    ax.fill(np.cos(theta), np.sin(theta), color=SLIDE_BLUE, alpha=0.10,
            linewidth=0)
    ax.plot(np.cos(theta), np.sin(theta), linestyle=(0, (4, 3)),
            color=SLIDE_BLUE, linewidth=1.7)
    ax.plot([0], [0], "o", markersize=5, color=SLIDE_BLUE)
    ang = np.deg2rad(35)
    ax.annotate(
        "",
        xy=(np.cos(ang), np.sin(ang)), xytext=(0, 0),
        arrowprops={"arrowstyle": "-", "color": SLIDE_GRAY, "linewidth": 1.2},
    )
    ax.text(0.38 * np.cos(ang), 0.38 * np.sin(ang) + 0.13, r"$\varepsilon$",
            fontsize=13, color=SLIDE_GRAY)
    ax.text(0.02, -0.24, r"$x$", fontsize=12, color=SLIDE_BLUE, ha="center")
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.45, 1.45)
    ax.set_aspect("equal")
    ax.set_title(r"$L=2$: a disc", fontsize=15, color=SLIDE_GRAY, pad=4)
    ax.axis("off")

    # --- L = 3: a ball -----------------------------------------------------
    ax = fig.add_subplot(gs[0, 2], projection="3d")
    u = np.linspace(0, 2 * np.pi, 60)
    v = np.linspace(0, np.pi, 40)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(xs, ys, zs, color=SLIDE_BLUE, alpha=0.13,
                    linewidth=0, antialiased=True, shade=False)
    ax.plot(np.cos(u), np.sin(u), 0, linestyle=(0, (4, 3)),
            color=SLIDE_BLUE, linewidth=1.1, alpha=0.65)

    # The radius is the same to every point of the boundary: three of them,
    # in unrelated directions, all of length epsilon.
    radii = [
        (0.0, 0.0, 1.0, (0.18, 0.10)),      # straight up
        (0.94, 0.34, 0.0, (0.05, -0.20)),   # equatorial, toward the viewer
        (-0.72, -0.24, -0.65, (-0.16, 0.16)),  # down and to the front
    ]
    for dx, dy, dz, (ox, oy) in radii:
        ax.plot([0, dx], [0, dy], [0, dz], color=SLIDE_GRAY,
                linewidth=1.2, zorder=6)
        ax.scatter([dx], [dy], [dz], s=11, color=SLIDE_GRAY, zorder=7)
        ax.text(0.55 * dx + ox, 0.55 * dy + oy, 0.55 * dz,
                r"$\varepsilon$", fontsize=14, color=SLIDE_GRAY,
                ha="center", va="center", zorder=8)

    ax.scatter([0], [0], [0], s=18, color=SLIDE_BLUE, zorder=9)
    ax.set_box_aspect((1, 1, 1), zoom=1.32)
    lim = 1.02
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    ax.set_title(r"$L=3$: a ball", fontsize=15, color=SLIDE_GRAY, pad=2)
    ax.set_axis_off()

    fig.subplots_adjust(left=0.01, right=0.99, top=0.87, bottom=0.05)
    save_vector_pair(fig, "open-balls")


def make_all() -> None:
    make_open_balls_plot()


if __name__ == "__main__":
    make_all()
