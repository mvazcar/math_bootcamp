"""Regenerate the math3 notebook plots as vector PDF/SVG assets.

The plotting logic is transcribed from UtilityPlots.ipynb and
convexity(2).ipynb. Existing PNG assets and notebooks are left untouched.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


OUTPUT_DIR = Path(__file__).resolve().parent
CHAD_BLUE = (0.1, 0.1, 0.5)
CHAD_GREEN = (0.0, 0.4, 0.0)
LEVELS = [0.5, 0.8, 1.2, 1.8, 2.6]
T_VALUES = [0.35, 0.50, 0.65, 0.80, 1.00]


plt.rcParams.update(
    {
        "font.size": 16,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "path",
    }
)


def blend_with_white(rgb: tuple[float, float, float], amount: float) -> tuple[float, ...]:
    white = np.array([1.0, 1.0, 1.0])
    return tuple(((1 - amount) * white + amount * np.array(rgb)).tolist())


COLORS = [blend_with_white(CHAD_BLUE, amount) for amount in T_VALUES]
LABELS = {level: f"$u={level}$" for level in LEVELS}


def save_vector_pair(fig: plt.Figure, stem: str) -> None:
    for suffix in ("pdf", "svg"):
        fig.savefig(
            OUTPUT_DIR / f"{stem}.{suffix}",
            bbox_inches="tight",
            facecolor="white",
        )
    plt.close(fig)


def make_2d_plot() -> None:
    x1 = np.linspace(0.1, 5, 300)
    x2 = np.linspace(0.1, 5, 300)
    x1_grid, x2_grid = np.meshgrid(x1, x2)
    utility = np.sqrt(x1_grid * x2_grid)

    fig, ax = plt.subplots(figsize=(7, 6))
    contours = ax.contour(
        x1_grid,
        x2_grid,
        utility,
        levels=LEVELS,
        colors=COLORS,
        linewidths=2,
    )
    ax.clabel(
        contours,
        inline=True,
        fontsize=9,
        fmt=LABELS,
        manual=[(level, level) for level in LEVELS],
    )
    ax.set_xlabel(r"$x_1$", color="black")
    ax.set_ylabel(r"$x_2$", color="black")
    ax.set_title(
        r"Indifference Curves: $u(x_1,x_2)=x_1^{1/2}x_2^{1/2}$",
        pad=30,
    )
    ax.grid(True, alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    handles = [
        Line2D([0], [0], color=COLORS[index], lw=2, label=LABELS[level])
        for index, level in enumerate(LEVELS)
    ]
    ax.legend(handles=handles, loc="upper right", frameon=False)
    fig.tight_layout()
    save_vector_pair(fig, "2d-plot")


def make_3d_plot() -> None:
    x1 = np.linspace(0.1, 5, 300)
    x2 = np.linspace(0.1, 5, 300)
    x1_grid, x2_grid = np.meshgrid(x1, x2)
    utility = np.sqrt(x1_grid * x2_grid)

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")
    surface_color = (CHAD_GREEN[0], CHAD_GREEN[1], CHAD_GREEN[2], 0.08)
    ax.plot_surface(
        x1_grid,
        x2_grid,
        utility,
        color=surface_color,
        rstride=4,
        cstride=4,
        linewidth=0.2,
        antialiased=True,
    )
    ax.contour(
        x1_grid,
        x2_grid,
        utility,
        levels=LEVELS,
        colors=COLORS,
        linewidths=2,
    )
    ax.set_xlabel(r"$x_1$", color="black")
    ax.set_ylabel(r"$x_2$", color="black")
    ax.set_zlabel(r"$u(x_1,x_2)$", color="black")
    ax.set_title(
        r"Utility Surface + Indifference Curves: "
        r"$u(x_1,x_2)=x_1^{1/2}x_2^{1/2}$",
        y=1.02,
    )
    fig.tight_layout()
    save_vector_pair(fig, "3d-plot")


def make_monotonicity_plot() -> None:
    x1 = np.linspace(0.1, 5, 400)
    x2 = np.linspace(0.1, 5, 400)
    x1_grid, x2_grid = np.meshgrid(x1, x2)
    utility = np.sqrt(x1_grid * x2_grid)

    fig, ax = plt.subplots(figsize=(7, 6))
    contours = ax.contour(
        x1_grid,
        x2_grid,
        utility,
        levels=LEVELS,
        colors=COLORS,
        linewidths=2,
    )
    ax.clabel(
        contours,
        inline=True,
        inline_spacing=1,
        use_clabeltext=True,
        fontsize=9,
        fmt=LABELS,
        manual=[(level, level) for level in LEVELS],
    )
    ax.scatter([1], [1], s=30, color="red", zorder=5)
    ax.annotate(
        "",
        xy=(1, 4.75),
        xytext=(1, 1),
        arrowprops={"arrowstyle": "->", "color": "red", "lw": 2},
    )
    ax.annotate(
        "",
        xy=(4.75, 1),
        xytext=(1, 1),
        arrowprops={"arrowstyle": "->", "color": "red", "lw": 2},
    )
    horizontal_text = ax.text(
        2.8,
        0.55,
        "If $x_1$ increases,\nutility will increase",
        color="red",
        fontsize=12,
        ha="center",
    )
    vertical_text = ax.text(
        0.65,
        3.0,
        "If $x_2$ increases,\nutility will increase",
        color="red",
        fontsize=12,
        va="center",
        rotation=90,
    )
    for text in (horizontal_text, vertical_text):
        text.set_path_effects(
            [
                path_effects.Stroke(linewidth=2.5, foreground="white"),
                path_effects.Normal(),
            ]
        )
    ax.set_xlabel(r"$x_1$", color="black")
    ax.set_ylabel(r"$x_2$", color="black")
    ax.set_title("Strict Monotonicity", pad=30)
    ax.grid(True, alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    handles = [
        Line2D([0], [0], color=COLORS[index], lw=2, label=LABELS[level])
        for index, level in enumerate(LEVELS)
    ]
    ax.legend(handles=handles, loc="upper right", frameon=False)
    fig.tight_layout()
    save_vector_pair(fig, "monotonicity")


if __name__ == "__main__":
    make_2d_plot()
    make_3d_plot()
    make_monotonicity_plot()
