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

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from palette import SLIDE_BLUE, SLIDE_GRAY  # noqa: E402


OUTPUT_DIR = Path(__file__).resolve().parent

PLOT_STEMS = ("neighborhood",)


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


def make_neighborhood_plot() -> None:
    """The epsilon-neighborhood of a on the real line.

    Open endpoints are drawn as hollow circles and the centre as a filled
    one, so the strict inequality in the definition is visible rather than
    only asserted.
    """
    eps = 1.0
    fig, ax = plt.subplots(figsize=(6.6, 0.66))

    # the line itself, with an arrowhead so it reads as all of R
    ax.annotate(
        "",
        xy=(2.35, 0), xytext=(-2.35, 0),
        arrowprops={"arrowstyle": "-|>", "color": SLIDE_GRAY, "linewidth": 1.1},
    )
    # the neighborhood, picked out on top of it
    ax.plot([-eps, eps], [0, 0], color=SLIDE_BLUE, linewidth=2.6,
            solid_capstyle="butt", zorder=2)

    # excluded endpoints hollow, the centre solid
    ax.plot([-eps, eps], [0, 0], "o", markersize=7, zorder=3,
            markerfacecolor="white", markeredgecolor=SLIDE_BLUE,
            markeredgewidth=1.8, linestyle="none")
    ax.plot([0], [0], "o", markersize=6, color=SLIDE_BLUE, zorder=4)

    for x, label in ((-eps, r"$a-\varepsilon$"), (0, r"$a$"), (eps, r"$a+\varepsilon$")):
        ax.text(x, -0.30, label, ha="center", va="top", fontsize=12,
                color=SLIDE_BLUE if x == 0 else "black")

    ax.set_xlim(-2.45, 2.45)
    ax.set_ylim(-0.82, 0.30)
    ax.axis("off")
    fig.tight_layout(pad=0.1)
    save_vector_pair(fig, "neighborhood")


def make_all() -> None:
    make_neighborhood_plot()


if __name__ == "__main__":
    make_all()
