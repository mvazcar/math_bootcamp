"""Regenerate the clean Day 3 Matplotlib figures as PDF and SVG assets.

Colours come from source/palette.py, shared with the slides.  The figure
sizes and type sizes are chosen for the final Beamer placements, so labels
remain readable after the vector art is scaled on a slide.
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from palette import SLIDE_BLUE, SLIDE_GREEN, SLIDE_RED, SLIDE_GRAY  # noqa: E402


OUTPUT_DIR = Path(__file__).resolve().parent

# Palette: see source/palette.py.

# Four levels rather than five: the two lowest curves used to meet in the
# bottom-left corner, where their labels collided.  These spread evenly along
# the diagonal, so every label sits clear of its neighbours.
LEVELS = [0.8, 1.4, 2.2, 3.2]
T_VALUES = [0.40, 0.58, 0.78, 1.00]
PLOT_STEMS = ("2d-plot", "3d-plot", "monotonicity")


plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 16,
        "mathtext.fontset": "cm",
        "axes.labelsize": 18,
        "xtick.labelsize": 13,
        "ytick.labelsize": 13,
        "axes.edgecolor": SLIDE_GRAY,
        "axes.linewidth": 0.8,
        "grid.color": SLIDE_GRAY,
        "grid.alpha": 0.18,
        "grid.linewidth": 0.6,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "path",
    }
)


def blend_with_white(rgb: tuple[float, float, float], amount: float) -> tuple[float, ...]:
    white = np.array([1.0, 1.0, 1.0])
    return tuple(((1 - amount) * white + amount * np.array(rgb)).tolist())


COLORS = [blend_with_white(SLIDE_BLUE, amount) for amount in T_VALUES]
LABELS = {level: f"$u={level}$" for level in LEVELS}


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


def style_2d_axes(ax: plt.Axes) -> None:
    ax.set_xlim(0.1, 5.0)
    ax.set_ylim(0.1, 5.0)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$", rotation=0, labelpad=12)
    ax.grid(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_aspect("equal", adjustable="box")


def utility_grid(points: int = 500) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x1 = np.linspace(0.1, 5.0, points)
    x2 = np.linspace(0.1, 5.0, points)
    x1_grid, x2_grid = np.meshgrid(x1, x2)
    return x1_grid, x2_grid, np.sqrt(x1_grid * x2_grid)


def add_utility_contours(
    ax: plt.Axes,
    x1: np.ndarray,
    x2: np.ndarray,
    utility: np.ndarray,
    *,
    show_labels: bool = True,
) -> None:
    contours = ax.contour(
        x1,
        x2,
        utility,
        levels=LEVELS,
        colors=COLORS,
        linewidths=2.2,
    )
    if show_labels:
        labels = ax.clabel(
            contours,
            inline=True,
            inline_spacing=3,
            use_clabeltext=True,
            fontsize=13,
            fmt=LABELS,
            manual=[(level, level) for level in LEVELS],
        )
        # A white halo keeps a label legible where a neighbouring curve passes
        # close behind it.
        for label in labels:
            label.set_path_effects(
                [
                    path_effects.Stroke(linewidth=2.7, foreground="white"),
                    path_effects.Normal(),
                ]
            )


def make_2d_plot() -> None:
    x1, x2, utility = utility_grid()
    fig, ax = plt.subplots(figsize=(4.25, 3.45))
    add_utility_contours(ax, x1, x2, utility)
    style_2d_axes(ax)
    fig.tight_layout(pad=0.35)
    save_vector_pair(fig, "2d-plot")


def make_3d_plot() -> None:
    x1, x2, utility = utility_grid(points=120)
    fig = plt.figure(figsize=(4.55, 3.55))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(
        x1,
        x2,
        utility,
        color=SLIDE_GREEN,
        alpha=0.11,
        rcount=42,
        ccount=42,
        linewidth=0,
        antialiased=True,
        shade=False,
    )
    ax.contour(
        x1,
        x2,
        utility,
        levels=LEVELS,
        colors=COLORS,
        linewidths=2.2,
    )
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_zlim(0, 5)
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.set_zticks([0, 1, 2, 3, 4, 5])
    ax.set_xlabel(r"$x_1$", labelpad=4)
    ax.set_ylabel(r"$x_2$", labelpad=4)
    ax.set_zlabel(r"$u(x_1,x_2)$", labelpad=5)
    ax.view_init(elev=25, azim=-58)
    # The default 3D framing leaves a wide empty margin, so the cube reads as
    # much smaller than the 2D axes beside it on the Utility Representation
    # slide.  Zooming fills that margin and matches the two panels by eye.
    ax.set_box_aspect((1, 1, 0.82), zoom=1.28)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1, 1, 1, 0))
        axis.pane.set_edgecolor((1, 1, 1, 0))
    ax.grid(True, alpha=0.18)
    fig.subplots_adjust(left=0.01, right=0.91, bottom=0.02, top=0.98)
    save_vector_pair(fig, "3d-plot")


def make_monotonicity_plot() -> None:
    x1, x2, utility = utility_grid()
    fig, ax = plt.subplots(figsize=(4.25, 3.45))
    add_utility_contours(ax, x1, x2, utility, show_labels=False)
    style_2d_axes(ax)

    ax.scatter([1], [1], s=34, color=SLIDE_RED, zorder=5)
    arrow = {"arrowstyle": "->", "color": SLIDE_RED, "lw": 2.2}
    ax.annotate("", xy=(1, 4.75), xytext=(1, 1), arrowprops=arrow)
    ax.annotate("", xy=(4.75, 1), xytext=(1, 1), arrowprops=arrow)

    # Single-line captions set outside the arrows.  The earlier two-line
    # versions ran across the curves; an opaque backing keeps these readable
    # wherever the lowest contour passes behind them.
    caption = {
        "color": SLIDE_RED,
        "fontsize": 12,
        "ha": "center",
        "va": "center",
        "bbox": {"facecolor": "white", "edgecolor": "none", "pad": 1.6},
    }
    ax.text(3.35, 0.42, r"more $x_1$ $\Rightarrow$ higher $u$", **caption)
    ax.text(0.42, 3.35, r"more $x_2$ $\Rightarrow$ higher $u$", rotation=90, **caption)

    fig.tight_layout(pad=0.35)
    save_vector_pair(fig, "monotonicity")


def make_all() -> None:
    make_2d_plot()
    make_3d_plot()
    make_monotonicity_plot()


if __name__ == "__main__":
    make_all()
