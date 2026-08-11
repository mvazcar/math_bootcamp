"""Regenerate every mathematical figure in the Day 5 deck.

The figure uses the exact palette and typography established in the earlier
utility and optimization notebooks.  It is exported as vector PDF and SVG.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = Path(__file__).resolve().parent

# Canonical notebook palette.
CHAD_BLUE = (0.1, 0.1, 0.5)
CHAD_GREEN = (0.0, 0.4, 0.0)
SIGNAL_RED = (1.0, 0.0, 0.0)
NEUTRAL_GRAY = (0.40, 0.40, 0.40)


plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 19,
        "mathtext.fontset": "cm",
        "axes.labelsize": 19,
        "xtick.labelsize": 13,
        "ytick.labelsize": 13,
        "axes.edgecolor": NEUTRAL_GRAY,
        "axes.linewidth": 0.8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "path",
    }
)


def blend_with_white(rgb: tuple[float, float, float], amount: float) -> tuple[float, ...]:
    white = np.array([1.0, 1.0, 1.0])
    return tuple(((1 - amount) * white + amount * np.array(rgb)).tolist())


CONTOUR_COLORS = [blend_with_white(CHAD_BLUE, value) for value in (0.48, 0.70, 1.00)]


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


def make_intertemporal_choice() -> None:
    """Plot the household's two-date tangency at a given interest rate."""
    beta = 0.80
    gross_return = 1.25
    present_value_wealth = 4.0

    # c_t + c_{t+1}/R = W.  With log utility, the selected parameters put
    # the optimum exactly on the 45-degree ray, which keeps the geometry clean.
    c_now_star = present_value_wealth / (1 + beta)
    c_next_star = beta * gross_return * c_now_star
    utility_star = np.log(c_now_star) + beta * np.log(c_next_star)

    fig, ax = plt.subplots(figsize=(5.25, 4.15))
    c_now = np.linspace(0.04, present_value_wealth, 500)
    budget = gross_return * (present_value_wealth - c_now)
    ax.plot(c_now, budget, color=NEUTRAL_GRAY, lw=2.7, zorder=3)

    grid = np.linspace(0.20, 4.95, 600)
    for offset, color in zip((-0.55, 0.0, 0.48), CONTOUR_COLORS):
        level = utility_star + offset
        contour = np.exp((level - np.log(grid)) / beta)
        visible = (contour >= 0) & (contour <= 5.15)
        ax.plot(grid[visible], contour[visible], color=color, lw=2.2)

    ax.scatter([c_now_star], [c_next_star], s=54, color=CHAD_GREEN, zorder=6)
    ax.text(
        c_now_star + 0.15,
        c_next_star - 0.42,
        r"$(c_t^*,c_{t+1}^*)$",
        color=CHAD_GREEN,
        ha="left",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.15},
        zorder=7,
    )

    # A short red segment makes the local price tradeoff visible without
    # adding a second competing line.
    delta = 0.42
    start = np.array([c_now_star + delta, c_next_star - gross_return * delta])
    end = np.array([c_now_star - delta, c_next_star + gross_return * delta])
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={
            "arrowstyle": "-|>",
            "color": SIGNAL_RED,
            "lw": 2.4,
            "mutation_scale": 13,
        },
    )
    ax.text(
        0.20,
        4.85,
        r"save one more unit today",
        color=SIGNAL_RED,
        ha="left",
        bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.12},
        zorder=8,
    )
    ax.text(
        3.15,
        1.16,
        "intertemporal budget",
        color=NEUTRAL_GRAY,
        rotation=-39,
        ha="center",
        va="bottom",
        bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.10},
        zorder=8,
    )
    ax.text(
        4.05,
        4.15,
        "higher lifetime utility",
        color=CHAD_BLUE,
        ha="right",
        bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.12},
        zorder=8,
    )

    ax.set_xlim(0, 4.25)
    ax.set_ylim(0, 5.25)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel(r"current consumption $c_t$", labelpad=6)
    ax.set_ylabel(r"future consumption $c_{t+1}$", rotation=90, labelpad=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(NEUTRAL_GRAY)
    ax.spines["bottom"].set_color(NEUTRAL_GRAY)
    fig.tight_layout(pad=0.25)
    save_vector_pair(fig, "intertemporal-choice")


def make_all() -> None:
    make_intertemporal_choice()


if __name__ == "__main__":
    make_all()
