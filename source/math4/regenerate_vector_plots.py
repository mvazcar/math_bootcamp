"""Regenerate every mathematical figure in the Day 4 deck.

All figures use the exact palette established in the earlier utility notebooks
and are exported as vector PDF and SVG files.  The flow diagram on slide 3 is
not a plot and remains native TikZ; every mathematical graph is generated here.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MplPath


OUTPUT_DIR = Path(__file__).resolve().parent

# Canonical notebook palette.
CHAD_BLUE = (0.1, 0.1, 0.5)
CHAD_GREEN = (0.0, 0.4, 0.0)
SIGNAL_RED = (1.0, 0.0, 0.0)
NEUTRAL_GRAY = (0.40, 0.40, 0.40)

PLOT_STEMS = (
    "foc-slope",
    "critical-points",
    "gradient-directions",
    "constraint-tangent",
    "crossing-level-set",
    "lagrange-tangency",
    "multiplier-relaxation",
    "leontief-kink",
)


plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 17,
        "mathtext.fontset": "cm",
        "axes.labelsize": 19,
        "xtick.labelsize": 13,
        "ytick.labelsize": 13,
        "axes.edgecolor": NEUTRAL_GRAY,
        "axes.linewidth": 0.8,
        "grid.color": NEUTRAL_GRAY,
        "grid.alpha": 0.16,
        "grid.linewidth": 0.6,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "path",
    }
)


def blend_with_white(rgb: tuple[float, float, float], amount: float) -> tuple[float, ...]:
    white = np.array([1.0, 1.0, 1.0])
    return tuple(((1 - amount) * white + amount * np.array(rgb)).tolist())


CONTOUR_COLORS = [blend_with_white(CHAD_BLUE, value) for value in (0.50, 0.72, 1.00)]


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


def setup_plane(
    ax: plt.Axes,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
    *,
    equal: bool = False,
) -> None:
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel(r"$x_1$", labelpad=4)
    ax.set_ylabel(r"$x_2$", rotation=0, labelpad=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(NEUTRAL_GRAY)
    ax.spines["bottom"].set_color(NEUTRAL_GRAY)
    if equal:
        ax.set_aspect("equal", adjustable="box")


def draw_arrow(
    ax: plt.Axes,
    start: tuple[float, float] | np.ndarray,
    end: tuple[float, float] | np.ndarray,
    color: tuple[float, float, float],
    *,
    linewidth: float = 2.4,
) -> None:
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={
            "arrowstyle": "-|>",
            "color": color,
            "lw": linewidth,
            "mutation_scale": 13,
            "shrinkA": 0,
            "shrinkB": 0,
        },
    )


def draw_ellipse(
    ax: plt.Axes,
    center: tuple[float, float],
    radii: tuple[float, float],
    color: tuple[float, ...],
) -> None:
    theta = np.linspace(0, 2 * np.pi, 400)
    x = center[0] + radii[0] * np.cos(theta)
    y = center[1] + radii[1] * np.sin(theta)
    ax.plot(x, y, color=color, lw=2.15)


def make_foc_slope() -> None:
    fig, ax = plt.subplots(figsize=(8.2, 3.9))
    x = np.linspace(-2.15, 2.15, 500)
    ax.plot(x, 4 - x**2, color=CHAD_BLUE, lw=3.0)

    for point, color in ((-1.2, SIGNAL_RED), (1.2, SIGNAL_RED)):
        y = 4 - point**2
        slope = -2 * point
        segment = np.linspace(point - 0.35, point + 0.35, 60)
        ax.plot(segment, y + slope * (segment - point), color=color, lw=2.6)
        ax.scatter([point], [y], s=54, color=color, zorder=5)

    ax.plot([-0.38, 0.38], [4, 4], color=CHAD_GREEN, lw=2.6)
    ax.scatter([0], [4], s=54, color=CHAD_GREEN, zorder=5)
    ax.plot([0, 0], [0, 4], color=NEUTRAL_GRAY, lw=1.0, ls="--")
    ax.axhline(0, color=NEUTRAL_GRAY, lw=0.9)

    ax.text(-1.2, 1.15, "$f'(x)>0$\nmove right", color=SIGNAL_RED, ha="center", va="center")
    ax.text(1.2, 1.15, "$f'(x)<0$\nmove left", color=SIGNAL_RED, ha="center", va="center")
    ax.text(0, 4.48, "$f'(x^*)=0$", color=CHAD_GREEN, ha="center", va="center")
    ax.text(0, -0.33, "$x^*$", ha="center", va="top")
    ax.text(2.25, -0.18, "$x$", ha="right", va="top")

    ax.set_xlim(-2.3, 2.3)
    ax.set_ylim(-0.55, 4.9)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout(pad=0.15)
    save_vector_pair(fig, "foc-slope")


def make_critical_points() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(9.2, 2.65))
    cases = (
        (lambda x: -(x**2), (-1.45, 1.45), (-2.1, 0.65), r"$f(x)=-x^2$", CHAD_GREEN, "local and global\nmaximum"),
        (lambda x: x**2, (-1.45, 1.45), (-0.65, 2.1), r"$f(x)=x^2$", SIGNAL_RED, "local and global\nminimum"),
        (lambda x: x**3, (-1.3, 1.3), (-2.1, 2.1), r"$f(x)=x^3$", NEUTRAL_GRAY, "neither"),
    )
    for ax, (function, xlim, ylim, formula, point_color, conclusion) in zip(axes, cases):
        x = np.linspace(xlim[0] * 0.92, xlim[1] * 0.92, 350)
        ax.plot(x, function(x), color=CHAD_BLUE, lw=3.0)
        ax.scatter([0], [0], s=52, color=point_color, zorder=5)
        ax.axhline(0, color=NEUTRAL_GRAY, lw=0.8)
        ax.axvline(0, color=NEUTRAL_GRAY, lw=0.8)
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_title(formula, fontsize=21, pad=3)
        ax.text(
            0.5,
            -0.18,
            conclusion,
            color=point_color,
            fontsize=17,
            ha="center",
            va="top",
            transform=ax.transAxes,
        )
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.26, top=0.86, wspace=0.34)
    save_vector_pair(fig, "critical-points")


def make_gradient_directions() -> None:
    fig, ax = plt.subplots(figsize=(4.5, 3.65))
    setup_plane(ax, (-0.2, 5.45), (-0.2, 4.8))
    center = (2.7, 2.35)
    for radius, color in zip((1.75, 1.2, 0.65), CONTOUR_COLORS):
        draw_ellipse(ax, center, (1.25 * radius, 0.78 * radius), color)

    point = np.array([1.55, 1.65])
    gradient_end = np.array([2.62, 2.30])
    direction_end = np.array([2.10, 1.15])
    ax.scatter(*point, s=38, color=NEUTRAL_GRAY, zorder=5)
    draw_arrow(ax, point, gradient_end, SIGNAL_RED)
    draw_arrow(ax, point, direction_end, CHAD_GREEN)
    ax.text(1.42, 1.48, "$x$", ha="right", va="top")
    ax.text(2.05, 2.42, r"$\nabla f(x)$", color=SIGNAL_RED, ha="center")
    ax.text(2.18, 1.08, "$d$", color=CHAD_GREEN, ha="left", va="top")
    ax.text(3.55, 4.05, "level sets of $f$", color=CHAD_BLUE, ha="center")
    fig.tight_layout(pad=0.25)
    save_vector_pair(fig, "gradient-directions")


def make_constraint_tangent() -> None:
    fig, ax = plt.subplots(figsize=(4.5, 3.65))
    setup_plane(ax, (-0.2, 5.45), (-0.2, 4.6))
    vertices = [(0.3, 0.7), (1.4, 2.5), (3.4, 1.2), (5.0, 3.4)]
    path = MplPath(
        vertices,
        [MplPath.MOVETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4],
    )
    ax.add_patch(PathPatch(path, fill=False, color=NEUTRAL_GRAY, lw=2.6))

    point = np.array([2.4625, 1.90])
    tangent = np.array([5.025, 1.05])
    tangent /= np.linalg.norm(tangent)
    normal = np.array([-tangent[1], tangent[0]])
    tangent_start = point - 1.05 * tangent
    tangent_end = point + 1.05 * tangent
    normal_end = point + 1.28 * normal

    ax.scatter(*point, s=38, color=NEUTRAL_GRAY, zorder=5)
    draw_arrow(ax, tangent_start, tangent_end, CHAD_GREEN)
    draw_arrow(ax, point, normal_end, SIGNAL_RED)
    ax.text(4.82, 3.43, "$g(x)=0$", ha="left", va="center")
    ax.text(2.52, 1.72, "$x$", ha="left", va="top")
    ax.text(*(tangent_end + np.array([0.08, 0.02])), "$d$", color=CHAD_GREEN, ha="left")
    ax.text(*(normal_end + np.array([-0.05, 0.04])), r"$\nabla g(x)$", color=SIGNAL_RED, ha="right")
    fig.tight_layout(pad=0.25)
    save_vector_pair(fig, "constraint-tangent")


def make_crossing_level_set() -> None:
    fig, ax = plt.subplots(figsize=(4.8, 3.75))
    setup_plane(ax, (-0.2, 6.65), (-0.2, 5.60))
    center = (4.1, 3.8)
    for radius, color in zip((2.1, 1.55, 1.0), CONTOUR_COLORS):
        draw_ellipse(ax, center, (1.15 * radius, 0.78 * radius), color)

    line_start = np.array([0.35, 4.35])
    line_end = np.array([5.65, 0.65])
    ax.plot(*zip(line_start, line_end), color=NEUTRAL_GRAY, lw=2.6)
    point = np.array([2.30, 2.99])
    direction = (line_end - line_start) / np.linalg.norm(line_end - line_start)
    improve_end = point + 1.15 * direction
    ax.scatter(*point, s=38, color=NEUTRAL_GRAY, zorder=5)
    draw_arrow(ax, point, improve_end, SIGNAL_RED)
    ax.text(5.52, 0.76, "$g(x)=0$", ha="left", va="top")
    ax.text(2.20, 2.83, "$x$", ha="right", va="top")
    ax.text(*(improve_end + np.array([0.08, -0.06])), "$d$", color=SIGNAL_RED, ha="left", va="top")
    ax.annotate(
        "higher $f$",
        xy=(4.18, 4.03),
        xytext=(4.85, 4.62),
        color=CHAD_BLUE,
        ha="center",
        arrowprops={"arrowstyle": "-|>", "color": CHAD_BLUE, "lw": 1.8},
    )
    fig.tight_layout(pad=0.25)
    save_vector_pair(fig, "crossing-level-set")


def make_lagrange_tangency() -> None:
    fig, ax = plt.subplots(figsize=(4.8, 3.75))
    setup_plane(ax, (-0.2, 6.8), (-0.2, 6.4), equal=True)
    center = np.array([4.0, 3.7])
    for radius, color in zip((2.6, 2.05, 1.5), CONTOUR_COLORS):
        draw_ellipse(ax, tuple(center), (radius, radius), color)

    point = np.array([2.8, 2.8])
    tangent = np.array([0.6, -0.8])
    line_start = point - 3.0 * tangent
    line_end = point + 3.0 * tangent
    ax.plot(*zip(line_start, line_end), color=NEUTRAL_GRAY, lw=2.6)
    ax.scatter(*point, s=40, color=NEUTRAL_GRAY, zorder=5)

    objective_end = point + np.array([1.05, 0.79])
    constraint_end = point - np.array([0.92, 0.69])
    draw_arrow(ax, point, objective_end, SIGNAL_RED)
    draw_arrow(ax, point, constraint_end, CHAD_GREEN)
    ax.text(4.55, 0.52, "$g(x)=0$", ha="left", va="top")
    ax.text(2.93, 2.72, "$x^*$", ha="left", va="top")
    ax.text(3.52, 3.72, r"$\nabla f(x^*)$", color=SIGNAL_RED, ha="center", va="bottom")
    ax.text(1.55, 1.68, r"$\lambda^*\nabla g(x^*)$", color=CHAD_GREEN, ha="center", va="top")
    ax.text(4.58, 4.58, "higher $f$", color=CHAD_BLUE, ha="center")
    fig.tight_layout(pad=0.25)
    save_vector_pair(fig, "lagrange-tangency")


def make_multiplier_relaxation() -> None:
    fig, ax = plt.subplots(figsize=(4.8, 3.2))
    center = (3.15, 2.35)
    for radii, color in zip(((1.75, 1.05), (1.28, 0.77), (0.82, 0.49)), CONTOUR_COLORS):
        draw_ellipse(ax, center, radii, color)

    x = np.array([0.35, 5.25])
    solid_y = np.array([3.35, 0.65])
    dashed_y = solid_y + 0.38
    ax.plot(x, solid_y, color=NEUTRAL_GRAY, lw=2.6)
    ax.plot(x, dashed_y, color=NEUTRAL_GRAY, lw=2.3, ls="--")
    ax.text(5.33, 0.61, "$c$", ha="left", va="top")
    ax.text(5.33, 1.08, r"$c+\Delta c$", ha="left", va="bottom")

    start = np.array([2.54, 2.04])
    end = np.array([2.79, 2.43])
    draw_arrow(ax, start, end, SIGNAL_RED)
    ax.text(2.96, 2.61, r"$\Delta F\approx\lambda^*\Delta c$", color=SIGNAL_RED, ha="left")
    ax.set_xlim(0.0, 6.15)
    ax.set_ylim(0.25, 4.05)
    ax.axis("off")
    fig.tight_layout(pad=0.12)
    save_vector_pair(fig, "multiplier-relaxation")


def make_leontief_kink() -> None:
    fig, ax = plt.subplots(figsize=(4.25, 3.6))
    setup_plane(ax, (0, 5.8), (0, 5.2), equal=True)
    for kink, color in zip((1.1, 1.8, 2.5), CONTOUR_COLORS):
        ax.plot([kink, kink, 5.5], [5.0, kink, kink], color=color, lw=2.25)

    ax.plot([0, 4.8], [0, 4.8], color=NEUTRAL_GRAY, lw=1.2, ls="--")
    ax.plot([0.4, 4.6], [4.6, 0.4], color=NEUTRAL_GRAY, lw=2.7)
    ax.scatter([2.5], [2.5], s=44, color=CHAD_GREEN, zorder=5)
    ax.text(4.05, 4.42, "$a x_1=b x_2$", color=NEUTRAL_GRAY, ha="left")
    ax.text(2.62, 2.38, "$x^*$", color=CHAD_GREEN, ha="left", va="top")
    fig.tight_layout(pad=0.25)
    save_vector_pair(fig, "leontief-kink")


def make_all() -> None:
    make_foc_slope()
    make_critical_points()
    make_gradient_directions()
    make_constraint_tangent()
    make_crossing_level_set()
    make_lagrange_tangency()
    make_multiplier_relaxation()
    make_leontief_kink()


if __name__ == "__main__":
    make_all()
