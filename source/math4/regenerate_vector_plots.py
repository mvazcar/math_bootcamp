"""Regenerate every mathematical figure in the optimization decks.

All figures use the shared palette in source/palette.py
and are exported as vector PDF and SVG files. Native schematic diagrams remain
in TikZ; every plotted mathematical object is generated here.
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from palette import SLIDE_BLUE, SLIDE_GREEN, SLIDE_RED, SLIDE_GRAY  # noqa: E402
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MplPath


OUTPUT_DIR = Path(__file__).resolve().parent

# Palette: see source/palette.py.

PLOT_STEMS = (
    "sundaram-global-local",
    "sundaram-foc-signs",
    "foc-slope",
    "critical-points",
    "gradient-directions",
    "constraint-tangent",
    "crossing-level-set",
    "lagrange-tangency",
    "lagrange-surface",
    "hessian-surfaces",
    "multiplier-relaxation",
    "multiplier-surface",
    "consumer-cases",
    "leontief-kink",
    "linear-demand",
    "ces-demand",
    "leontief-demand",
    "weierstrass-failures",
    "boundary-candidates",
    "kkt-regimes",
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
        "axes.edgecolor": SLIDE_GRAY,
        "axes.linewidth": 0.8,
        "grid.color": SLIDE_GRAY,
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


CONTOUR_COLORS = [blend_with_white(SLIDE_BLUE, value) for value in (0.50, 0.72, 1.00)]


def linear_utility(bundle: np.ndarray, alpha: float) -> float:
    return float(alpha * bundle[0] + (1 - alpha) * bundle[1])


def ces_utility(bundle: np.ndarray, rho: float) -> float:
    return float((bundle[0] ** rho + bundle[1] ** rho) ** (1 / rho))


def ces_walrasian(prices: np.ndarray, income: float, rho: float) -> np.ndarray:
    sigma = 1 / (1 - rho)
    price_sum = np.sum(prices ** (1 - sigma))
    return income * prices ** (-sigma) / price_sum


def leontief_utility(bundle: np.ndarray, alpha: float) -> float:
    return float(min(alpha * bundle[0], (1 - alpha) * bundle[1]))


def leontief_walrasian(prices: np.ndarray, income: float, alpha: float) -> np.ndarray:
    denominator = (1 - alpha) * prices[0] + alpha * prices[1]
    return np.array(
        [
            (1 - alpha) * income / denominator,
            alpha * income / denominator,
        ]
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
    ax.spines["left"].set_color(SLIDE_GRAY)
    ax.spines["bottom"].set_color(SLIDE_GRAY)
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


def make_sundaram_global_local() -> None:
    """Recreate Sundaram Fig. 4.1: one local and one global maximum."""
    x = np.linspace(0.15, 9.65, 900)
    y = (
        0.48
        + 2.20 * np.exp(-0.5 * ((x - 2.35) / 0.88) ** 2)
        + 3.10 * np.exp(-0.5 * ((x - 7.75) / 1.15) ** 2)
        - 0.42 * np.exp(-0.5 * ((x - 0.55) / 0.30) ** 2)
    )
    x_local = x[(x > 1.7) & (x < 3.1)][np.argmax(y[(x > 1.7) & (x < 3.1)])]
    x_global = x[(x > 6.6) & (x < 8.8)][np.argmax(y[(x > 6.6) & (x < 8.8)])]
    y_local = np.interp(x_local, x, y)
    y_global = np.interp(x_global, x, y)

    fig, ax = plt.subplots(figsize=(7.4, 3.65))
    ax.plot(x, y, color=SLIDE_BLUE, lw=3.0)
    ax.scatter([x[0], x[-1]], [y[0], y[-1]], color=SLIDE_GRAY, s=28, zorder=5)
    for point_x, point_y, label in (
        (x_local, y_local, r"$x^*$"),
        (x_global, y_global, r"$y^*$"),
    ):
        ax.plot([point_x, point_x], [0, point_y], color=SLIDE_GRAY, lw=1.25, ls="--")
        ax.text(point_x, -0.18, label, ha="center", va="top")

    ax.plot([x[0], x[-1]], [0, 0], color=SLIDE_GRAY, lw=1.4)
    ax.annotate("", xy=(9.95, 0), xytext=(x[0], 0), arrowprops={"arrowstyle": "->", "color": SLIDE_GRAY, "lw": 1.4})
    ax.annotate("", xy=(x[0], 4.45), xytext=(x[0], 0), arrowprops={"arrowstyle": "->", "color": SLIDE_GRAY, "lw": 1.4})
    ax.text(5.0, -0.58, r"$D$", ha="center", va="top")
    ax.text(x_local, y_local + 0.18, "local", color=SLIDE_BLUE, ha="center", va="bottom")
    ax.text(x_global, y_global + 0.18, "global", color=SLIDE_BLUE, ha="center", va="bottom")
    ax.set_xlim(-0.15, 10.10)
    ax.set_ylim(-0.72, 4.55)
    ax.axis("off")
    fig.tight_layout(pad=0.16)
    save_vector_pair(fig, "sundaram-global-local")


def make_sundaram_foc_signs() -> None:
    """Recreate Sundaram Fig. 4.2: nonzero slope permits improvement."""
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.20))
    x = np.linspace(0.25, 4.75, 500)
    left = 0.95 + 1.95 * np.log1p(x)
    right = 4.65 - 0.48 * (x - 0.25) ** 1.35

    for ax, curve, point_x, formula, direction in (
        (axes[0], left, 2.55, r"$f'(x^*)>0$", 1),
        (axes[1], right, 2.75, r"$f'(x^*)<0$", -1),
    ):
        point_y = np.interp(point_x, x, curve)
        slope = np.gradient(curve, x)[np.argmin(np.abs(x - point_x))]
        tangent_x = np.linspace(point_x - 0.72, point_x + 0.72, 80)
        tangent_y = point_y + slope * (tangent_x - point_x)
        ax.plot(x, curve, color=SLIDE_BLUE, lw=3.0)
        ax.plot(tangent_x, tangent_y, color=SLIDE_GRAY, lw=1.8)
        ax.plot([point_x, point_x], [0, point_y], color=SLIDE_GRAY, lw=1.2, ls="--")
        ax.text(point_x, -0.16, r"$x^*$", ha="center", va="top")
        ax.text(point_x + 0.10 * direction, point_y + 0.50, formula, color=SLIDE_BLUE, ha="center")
        arrow_end = point_x + 0.72 * direction
        arrow_y = np.interp(arrow_end, x, curve)
        ax.annotate("", xy=(arrow_end, arrow_y), xytext=(point_x, point_y), arrowprops={"arrowstyle": "-|>", "color": SLIDE_GREEN, "lw": 2.2})
        ax.plot([0.05, 5.0], [0, 0], color=SLIDE_GRAY, lw=1.35)
        ax.annotate("", xy=(5.12, 0), xytext=(0.05, 0), arrowprops={"arrowstyle": "->", "color": SLIDE_GRAY, "lw": 1.35})
        ax.annotate("", xy=(0.05, 5.10), xytext=(0.05, 0), arrowprops={"arrowstyle": "->", "color": SLIDE_GRAY, "lw": 1.35})
        ax.set_xlim(-0.15, 5.25)
        ax.set_ylim(-0.58, 5.15)
        ax.axis("off")

    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.08, top=0.98, wspace=0.18)
    save_vector_pair(fig, "sundaram-foc-signs")


def make_foc_slope() -> None:
    fig, ax = plt.subplots(figsize=(8.2, 3.9))
    x = np.linspace(-2.15, 2.15, 500)
    ax.plot(x, 4 - x**2, color=SLIDE_BLUE, lw=3.0)

    for point, color in ((-1.2, SLIDE_RED), (1.2, SLIDE_RED)):
        y = 4 - point**2
        slope = -2 * point
        segment = np.linspace(point - 0.35, point + 0.35, 60)
        ax.plot(segment, y + slope * (segment - point), color=color, lw=2.6)
        ax.scatter([point], [y], s=54, color=color, zorder=5)

    ax.plot([-0.38, 0.38], [4, 4], color=SLIDE_GREEN, lw=2.6)
    ax.scatter([0], [4], s=54, color=SLIDE_GREEN, zorder=5)
    ax.plot([0, 0], [0, 4], color=SLIDE_GRAY, lw=1.0, ls="--")
    ax.axhline(0, color=SLIDE_GRAY, lw=0.9)

    ax.text(-1.2, 1.15, "$f'(x)>0$\nmove right", color=SLIDE_RED, ha="center", va="center")
    ax.text(1.2, 1.15, "$f'(x)<0$\nmove left", color=SLIDE_RED, ha="center", va="center")
    ax.text(0, 4.48, "$f'(x^*)=0$", color=SLIDE_GREEN, ha="center", va="center")
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
        (lambda x: -(x**2), (-1.45, 1.45), (-2.1, 0.65), r"$f(x)=-x^2$", SLIDE_GREEN, "local and global\nmaximum"),
        (lambda x: x**2, (-1.45, 1.45), (-0.65, 2.1), r"$f(x)=x^2$", SLIDE_RED, "local and global\nminimum"),
        (lambda x: x**3, (-1.3, 1.3), (-2.1, 2.1), r"$f(x)=x^3$", SLIDE_GRAY, "neither"),
    )
    for ax, (function, xlim, ylim, formula, point_color, conclusion) in zip(axes, cases):
        x = np.linspace(xlim[0] * 0.92, xlim[1] * 0.92, 350)
        ax.plot(x, function(x), color=SLIDE_BLUE, lw=3.0)
        ax.scatter([0], [0], s=52, color=point_color, zorder=5)
        ax.axhline(0, color=SLIDE_GRAY, lw=0.8)
        ax.axvline(0, color=SLIDE_GRAY, lw=0.8)
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
    ax.scatter(*point, s=38, color=SLIDE_GRAY, zorder=5)
    draw_arrow(ax, point, gradient_end, SLIDE_RED)
    draw_arrow(ax, point, direction_end, SLIDE_GREEN)
    ax.text(1.42, 1.48, "$x$", ha="right", va="top")
    ax.text(2.05, 2.42, r"$\nabla f(x)$", color=SLIDE_RED, ha="center")
    ax.text(2.18, 1.08, "$d$", color=SLIDE_GREEN, ha="left", va="top")
    ax.text(3.55, 4.05, "level sets of $f$", color=SLIDE_BLUE, ha="center")
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
    ax.add_patch(PathPatch(path, fill=False, color=SLIDE_GRAY, lw=2.6))

    point = np.array([2.4625, 1.90])
    tangent = np.array([5.025, 1.05])
    tangent /= np.linalg.norm(tangent)
    normal = np.array([-tangent[1], tangent[0]])
    tangent_start = point - 1.05 * tangent
    tangent_end = point + 1.05 * tangent
    normal_end = point + 1.28 * normal

    ax.scatter(*point, s=38, color=SLIDE_GRAY, zorder=5)
    draw_arrow(ax, tangent_start, tangent_end, SLIDE_GREEN)
    draw_arrow(ax, point, normal_end, SLIDE_RED)
    ax.text(4.82, 3.43, "$g(x)=0$", ha="left", va="center")
    ax.text(2.52, 1.72, "$x$", ha="left", va="top")
    ax.text(*(tangent_end + np.array([0.08, 0.02])), "$d$", color=SLIDE_GREEN, ha="left")
    ax.text(*(normal_end + np.array([-0.05, 0.04])), r"$\nabla g(x)$", color=SLIDE_RED, ha="right")
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
    ax.plot(*zip(line_start, line_end), color=SLIDE_GRAY, lw=2.6)
    point = np.array([2.30, 2.99])
    direction = (line_end - line_start) / np.linalg.norm(line_end - line_start)
    improve_end = point + 1.15 * direction
    ax.scatter(*point, s=38, color=SLIDE_GRAY, zorder=5)
    draw_arrow(ax, point, improve_end, SLIDE_RED)
    ax.text(5.52, 0.76, "$g(x)=0$", ha="left", va="top")
    ax.text(2.20, 2.83, "$x$", ha="right", va="top")
    ax.text(*(improve_end + np.array([0.08, -0.06])), "$d$", color=SLIDE_RED, ha="left", va="top")
    ax.annotate(
        "higher $f$",
        xy=(4.18, 4.03),
        xytext=(4.85, 4.62),
        color=SLIDE_BLUE,
        ha="center",
        arrowprops={"arrowstyle": "-|>", "color": SLIDE_BLUE, "lw": 1.8},
    )
    fig.tight_layout(pad=0.25)
    save_vector_pair(fig, "crossing-level-set")


def make_lagrange_tangency() -> None:
    fig, ax = plt.subplots(figsize=(4.8, 3.75))
    setup_plane(ax, (-0.2, 6.8), (-0.2, 6.4), equal=True)
    ax.set_xlabel("$x$", labelpad=4)
    ax.set_ylabel("$y$", rotation=0, labelpad=10)
    center = np.array([4.0, 3.7])
    for radius, color in zip((2.6, 2.05, 1.5), CONTOUR_COLORS):
        draw_ellipse(ax, tuple(center), (radius, radius), color)

    point = np.array([2.8, 2.8])
    tangent = np.array([0.6, -0.8])
    line_start = point - 3.0 * tangent
    line_end = point + 3.0 * tangent
    ax.plot(*zip(line_start, line_end), color=SLIDE_GRAY, lw=2.6)
    ax.scatter(*point, s=40, color=SLIDE_GRAY, zorder=5)

    # Keep this diagram in scalar coordinate notation.  It communicates only
    # the shared tangent; the slide derives the equality of the two slopes.
    ax.text(4.55, 0.52, "$g(x,y)=0$", ha="left", va="top")
    ax.text(2.92, 2.69, "$(x^*,y^*)$", ha="left", va="top")
    ax.text(1.15, 4.92, "$f(x,y)=\\bar f$", color=SLIDE_BLUE, ha="left")
    ax.text(4.58, 4.58, "higher $f$", color=SLIDE_BLUE, ha="center")
    ax.annotate(
        "same tangent",
        xy=(2.24, 3.55),
        xytext=(0.58, 5.62),
        color=SLIDE_GRAY,
        ha="left",
        arrowprops={"arrowstyle": "-|>", "color": SLIDE_GRAY, "lw": 1.5},
    )
    fig.tight_layout(pad=0.25)
    save_vector_pair(fig, "lagrange-tangency")


def make_lagrange_surface() -> None:
    """Show the constrained optimum as height along a feasible curve.

    The styling deliberately follows the Day 3 utility-surface figure: a very
    transparent Chad Green surface, Chad Blue level curves, transparent panes,
    and the same camera angle.  The additional gray plane is the equality
    constraint, while the bold blue intersection is the feasible curve.
    """
    grid = np.linspace(0, 2, 120)
    x1, x2 = np.meshgrid(grid, grid)
    objective = 4 - (x1 - 1) ** 2 - (x2 - 1) ** 2

    fig = plt.figure(figsize=(5.55, 4.25))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(
        x1,
        x2,
        objective,
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
        objective,
        levels=(3.0, 3.5, 3.92),
        colors=CONTOUR_COLORS,
        linewidths=2.0,
    )

    # The vertical plane g(x)=x_1+x_2-1.6=0.
    feasible_parameter = np.linspace(0, 1.6, 180)
    plane_height = np.linspace(2.05, 4.12, 2)
    plane_x1, plane_z = np.meshgrid(feasible_parameter, plane_height)
    plane_x2 = 1.6 - plane_x1
    ax.plot_surface(
        plane_x1,
        plane_x2,
        plane_z,
        color=SLIDE_GRAY,
        alpha=0.13,
        linewidth=0,
        shade=False,
    )

    # Lift the feasible line onto the objective surface.
    curve_x1 = feasible_parameter
    curve_x2 = 1.6 - feasible_parameter
    curve_z = 4 - (curve_x1 - 1) ** 2 - (curve_x2 - 1) ** 2
    ax.plot(curve_x1, curve_x2, curve_z, color=SLIDE_BLUE, lw=3.2, zorder=7)

    optimum = np.array([0.8, 0.8, 3.92])
    tangent_parameter = np.linspace(-0.30, 0.30, 40)
    ax.plot(
        optimum[0] + tangent_parameter,
        optimum[1] - tangent_parameter,
        np.full_like(tangent_parameter, optimum[2]),
        color=SLIDE_RED,
        lw=2.7,
        zorder=9,
    )
    ax.scatter(*optimum, s=52, color=SLIDE_RED, depthshade=False, zorder=10)
    ax.text(0.72, 0.68, 4.08, r"$x^*$", color=SLIDE_RED, ha="right", fontsize=14)
    ax.text(1.34, 0.22, 2.32, r"$g(x)=0$", color=SLIDE_GRAY, ha="center", fontsize=13)
    ax.text(0.34, 1.10, 4.08, "tangent", color=SLIDE_RED, ha="center", fontsize=11)

    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_zlim(2, 4.18)
    ax.set_xticks([0, 1, 2])
    ax.set_yticks([0, 1, 2])
    ax.set_zticks([2, 3, 4])
    ax.set_xlabel(r"$x_1$", labelpad=4)
    ax.set_ylabel(r"$x_2$", labelpad=4)
    ax.set_zlabel(r"$f(x_1,x_2)$", labelpad=5)
    ax.view_init(elev=25, azim=-58)
    ax.set_box_aspect((1, 1, 0.82))
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1, 1, 1, 0))
        axis.pane.set_edgecolor((1, 1, 1, 0))
    ax.grid(True, alpha=0.18)
    fig.subplots_adjust(left=0.01, right=0.92, bottom=0.02, top=0.98)
    save_vector_pair(fig, "lagrange-surface")


def make_hessian_surfaces() -> None:
    """Visualize the three strict sign patterns of a two-dimensional Hessian."""
    grid = np.linspace(-1.35, 1.35, 95)
    x1, x2 = np.meshgrid(grid, grid)
    cases = (
        ("negative definite", -(x1**2 + x2**2), SLIDE_BLUE, "strict local maximum"),
        ("positive definite", x1**2 + x2**2, SLIDE_GREEN, "strict local minimum"),
        ("indefinite", x1**2 - x2**2, SLIDE_GRAY, "neither"),
    )

    fig = plt.figure(figsize=(9.15, 3.35))
    for index, (title, surface, color, conclusion) in enumerate(cases, start=1):
        ax = fig.add_subplot(1, 3, index, projection="3d")
        ax.plot_surface(
            x1,
            x2,
            surface,
            color=color,
            alpha=0.24,
            rcount=40,
            ccount=40,
            linewidth=0,
            antialiased=True,
            shade=False,
        )
        ax.plot_wireframe(
            x1,
            x2,
            surface,
            rstride=12,
            cstride=12,
            color=color,
            linewidth=0.45,
            alpha=0.45,
        )
        ax.scatter([0], [0], [0], s=24, color=SLIDE_RED, depthshade=False, zorder=10)
        ax.set_xlim(-1.35, 1.35)
        ax.set_ylim(-1.35, 1.35)
        ax.set_zlim(-3.7, 3.7)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.set_xlabel(r"$x_1$", labelpad=-8)
        ax.set_ylabel(r"$x_2$", labelpad=-8)
        ax.set_title(title, fontsize=17, color=color, pad=0)
        ax.text2D(
            0.5,
            -0.10,
            conclusion,
            transform=ax.transAxes,
            ha="center",
            va="top",
            fontsize=15,
        )
        ax.view_init(elev=24, azim=-58)
        ax.set_box_aspect((1, 1, 0.78))
        for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
            axis.pane.set_facecolor((1, 1, 1, 0))
            axis.pane.set_edgecolor((1, 1, 1, 0))
        ax.grid(False)

    fig.subplots_adjust(left=0.005, right=0.995, bottom=0.14, top=0.90, wspace=0.02)
    save_vector_pair(fig, "hessian-surfaces")


def make_multiplier_relaxation() -> None:
    fig, ax = plt.subplots(figsize=(4.8, 3.2))
    center = (3.15, 2.35)
    for radii, color in zip(((1.75, 1.05), (1.28, 0.77), (0.82, 0.49)), CONTOUR_COLORS):
        draw_ellipse(ax, center, radii, color)

    x = np.array([0.35, 5.25])
    solid_y = np.array([3.35, 0.65])
    dashed_y = solid_y + 0.38
    ax.plot(x, solid_y, color=SLIDE_GRAY, lw=2.6)
    ax.plot(x, dashed_y, color=SLIDE_GRAY, lw=2.3, ls="--")
    ax.text(5.33, 0.61, "$c$", ha="left", va="top")
    ax.text(5.33, 1.08, r"$c+\Delta c$", ha="left", va="bottom")

    start = np.array([2.54, 2.04])
    end = np.array([2.79, 2.43])
    draw_arrow(ax, start, end, SLIDE_RED)
    ax.text(2.86, 2.72, r"$\Delta F$", color=SLIDE_RED, ha="left", fontsize=15)
    ax.set_xlim(0.0, 6.15)
    ax.set_ylim(0.25, 4.05)
    ax.axis("off")
    fig.tight_layout(pad=0.12)
    save_vector_pair(fig, "multiplier-relaxation")


def make_consumer_cases() -> None:
    """Reuse Day 3 indifference-curve styling for the three demand cases."""
    fig, axes = plt.subplots(1, 3, figsize=(9.2, 3.15))
    limit = 4.55
    budget_x = np.linspace(0, 4, 300)
    budget_y = 4 - budget_x

    for ax in axes:
        setup_plane(ax, (-0.12, limit), (-0.12, limit), equal=True)
        ax.plot(budget_x, budget_y, color=SLIDE_GRAY, lw=2.6, zorder=4)

    # Cobb-Douglas: the budget is tangent to the highest attainable contour.
    ax = axes[0]
    positive_x = np.linspace(0.12, limit, 500)
    for level, color in zip((1.2, 2.0, 2.7), CONTOUR_COLORS):
        contour_y = level**2 / positive_x
        visible = contour_y <= limit
        ax.plot(positive_x[visible], contour_y[visible], color=color, lw=2.2)
    ax.scatter([2], [2], s=44, color=SLIDE_GREEN, zorder=6)
    ax.text(2.13, 1.87, r"$x^*$", color=SLIDE_GREEN, ha="left", va="top")
    ax.set_title("Cobb-Douglas\nsmooth tangency", fontsize=17, pad=6)

    # Perfect substitutes: the objective slope selects one budget endpoint.
    ax = axes[1]
    line_x = np.linspace(0, limit, 500)
    for level, color in zip((3.5, 5.5, 8.0), CONTOUR_COLORS):
        line_y = level - 2 * line_x
        visible = (line_y >= 0) & (line_y <= limit)
        ax.plot(line_x[visible], line_y[visible], color=color, lw=2.2)
    ax.scatter([4], [0], s=44, color=SLIDE_GREEN, zorder=6)
    ax.text(3.83, 0.22, r"$x^*$", color=SLIDE_GREEN, ha="right", va="bottom")
    ax.set_title("Perfect substitutes\ncorner", fontsize=17, pad=6)

    # Leontief: fixed proportions select the kink on the budget line.
    ax = axes[2]
    for kink, color in zip((1.0, 2.0, 3.0), CONTOUR_COLORS):
        ax.plot([kink, kink, limit], [limit, kink, kink], color=color, lw=2.2)
    ax.plot([0, limit], [0, limit], color=SLIDE_GRAY, lw=1.1, ls="--")
    ax.scatter([2], [2], s=44, color=SLIDE_GREEN, zorder=6)
    ax.text(2.13, 1.87, r"$x^*$", color=SLIDE_GREEN, ha="left", va="top")
    ax.set_title("Leontief\nkink", fontsize=17, pad=6)

    fig.subplots_adjust(left=0.025, right=0.985, bottom=0.12, top=0.82, wspace=0.30)
    save_vector_pair(fig, "consumer-cases")


def make_leontief_kink() -> None:
    fig, ax = plt.subplots(figsize=(4.25, 3.6))
    setup_plane(ax, (0, 5.8), (0, 5.2), equal=True)
    for kink, color in zip((1.1, 1.8, 2.5), CONTOUR_COLORS):
        ax.plot([kink, kink, 5.5], [5.0, kink, kink], color=color, lw=2.25)

    ax.plot([0, 4.8], [0, 4.8], color=SLIDE_GRAY, lw=1.2, ls="--")
    ax.plot([0.4, 4.6], [4.6, 0.4], color=SLIDE_GRAY, lw=2.7)
    ax.scatter([2.5], [2.5], s=44, color=SLIDE_GREEN, zorder=5)
    ax.text(4.05, 4.42, "$a x_1=b x_2$", color=SLIDE_GRAY, ha="left")
    ax.text(2.62, 2.38, "$x^*$", color=SLIDE_GREEN, ha="left", va="top")
    fig.tight_layout(pad=0.25)
    save_vector_pair(fig, "leontief-kink")


def setup_consumer_example(
    ax: plt.Axes,
    prices: np.ndarray,
    income: float,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
    *,
    show_budget_label: bool = True,
) -> None:
    """Use one geometry for every demand example."""
    setup_plane(ax, xlim, ylim)
    p1, p2 = prices
    budget_x = np.linspace(0, income / p1, 500)
    budget_y = (income - p1 * budget_x) / p2
    ax.plot(budget_x, budget_y, color=SLIDE_GRAY, lw=2.7, zorder=4)
    if show_budget_label:
        label_x = 0.25 * income / p1
        label_y = 0.75 * income / p2 + 0.10
        ax.text(
            label_x,
            label_y,
            r"$p_1x_1+p_2x_2=m$",
            color=SLIDE_GRAY,
            ha="center",
            va="bottom",
            rotation=np.degrees(np.arctan(-p1 / p2)),
        )


def mark_consumer_optimum(
    ax: plt.Axes,
    optimum: tuple[float, float],
    *,
    label_offset: tuple[float, float] = (0.13, 0.13),
) -> None:
    ax.scatter(*optimum, s=48, color=SLIDE_GREEN, zorder=8)
    ax.text(
        optimum[0] + label_offset[0],
        optimum[1] + label_offset[1],
        r"$x^*$",
        color=SLIDE_GREEN,
        ha="left",
        va="bottom",
    )


def make_linear_demand() -> None:
    """Knife-edge interior solution for linear utility."""
    alpha = 0.4
    prices = np.array([2.0, 3.0])
    income = 12.0
    if not np.isclose(alpha / prices[0], (1 - alpha) / prices[1]):
        raise ValueError("The linear example requires the interior knife edge.")
    optimum = np.array([income / (2 * prices[0]), income / (2 * prices[1])])
    target_utility = linear_utility(optimum, alpha)

    fig, ax = plt.subplots(figsize=(5.0, 3.75))
    setup_consumer_example(
        ax,
        prices,
        income,
        (-0.15, 6.45),
        (-0.12, 4.45),
        show_budget_label=False,
    )
    x1 = np.linspace(0, 6.4, 500)
    for level, color in zip((1.5, target_utility, 3.0), CONTOUR_COLORS):
        x2 = (level - alpha * x1) / (1 - alpha)
        visible = (x2 >= 0) & (x2 <= 4.45)
        ax.plot(x1[visible], x2[visible], color=color, lw=2.2, zorder=3)

    # At alpha / p_1 = (1-alpha) / p_2, the entire budget line is optimal.
    budget_x = np.linspace(0, income / prices[0], 400)
    budget_y = (income - prices[0] * budget_x) / prices[1]
    ax.plot(budget_x, budget_y, color=SLIDE_GREEN, lw=3.0, alpha=0.68, zorder=6)
    mark_consumer_optimum(ax, tuple(optimum))
    ax.text(
        4.52,
        0.80,
        r"$2x_1+3x_2=12$, $u=2.4$: all optimal",
        color=SLIDE_GREEN,
        ha="center",
        va="top",
    )
    fig.tight_layout(pad=0.22)
    save_vector_pair(fig, "linear-demand")


def make_ces_demand() -> None:
    """Interior tangency for rho=1/2 CES utility."""
    rho = 0.5
    prices = np.array([1.0, 2.0])
    income = 6.0
    optimum = ces_walrasian(prices, income, rho)
    target_utility = ces_utility(optimum, rho)

    fig, ax = plt.subplots(figsize=(5.0, 3.75))
    setup_consumer_example(ax, prices, income, (-0.15, 6.45), (-0.12, 4.45))
    x1 = np.linspace(0, 6.4, 700)
    for level, color in zip((5.5, target_utility, 12.5), CONTOUR_COLORS):
        root_gap = np.maximum(level ** rho - x1**rho, 0)
        x2 = root_gap ** (1 / rho)
        visible = (x1 <= level) & (x2 <= 4.45)
        ax.plot(x1[visible], x2[visible], color=color, lw=2.2, zorder=3)

    mark_consumer_optimum(ax, tuple(optimum), label_offset=(0.16, 0.10))
    ax.text(4.82, 0.94, r"$u=9$", color=SLIDE_BLUE, ha="left", va="bottom")
    fig.tight_layout(pad=0.22)
    save_vector_pair(fig, "ces-demand")


def make_leontief_demand() -> None:
    """Positive kink solution for alpha=0.4 Leontief utility."""
    alpha = 0.4
    prices = np.array([1.0, 2.0])
    income = 7.0
    optimum = leontief_walrasian(prices, income, alpha)
    target_utility = leontief_utility(optimum, alpha)

    fig, ax = plt.subplots(figsize=(5.0, 3.75))
    setup_consumer_example(ax, prices, income, (-0.15, 7.45), (-0.12, 4.15))
    for level, color in zip((0.6, target_utility, 1.8), CONTOUR_COLORS):
        kink_x1 = level / alpha
        kink_x2 = level / (1 - alpha)
        ax.plot(
            [kink_x1, kink_x1, 7.4],
            [4.1, kink_x2, kink_x2],
            color=color,
            lw=2.2,
            zorder=3,
        )

    ray_x1 = np.linspace(0, 5.25, 200)
    ray_x2 = alpha * ray_x1 / (1 - alpha)
    ax.plot(ray_x1, ray_x2, color=SLIDE_GRAY, lw=1.15, ls="--", zorder=2)
    mark_consumer_optimum(ax, tuple(optimum))
    ax.text(5.40, 2.12, r"$u=1.2$", color=SLIDE_BLUE, ha="left", va="bottom")
    fig.tight_layout(pad=0.22)
    save_vector_pair(fig, "leontief-demand")




def make_weierstrass_failures() -> None:
    """Weierstrass as an implication, and what breaks when an assumption goes.

    Four panels: all assumptions holding, then each one dropped in turn.  Every
    panel states the antecedent and the consequent, so the slide reads as a row
    of implications rather than a row of pictures.
    """
    fig, axes = plt.subplots(1, 4, figsize=(11.2, 2.95))

    # 1. Compact domain, continuous function: both extremes attained.
    ax = axes[0]
    x = np.linspace(-1.0, 2.0, 300)
    ax.plot(x, x**2, color=SLIDE_BLUE, lw=3.0)
    ax.scatter([0], [0], s=52, color=SLIDE_GREEN, zorder=5)
    ax.scatter([2], [4], s=52, color=SLIDE_GREEN, zorder=5)
    ax.scatter([-1], [1], s=30, color=SLIDE_BLUE, zorder=5)
    ax.set_xlim(-1.45, 2.45)
    ax.set_ylim(-0.8, 4.9)

    # 2. Unbounded domain: the function runs away.
    ax = axes[1]
    x = np.linspace(-1.95, 1.95, 300)
    ax.plot(x, x**2, color=SLIDE_BLUE, lw=3.0)
    for tip in (-1.95, 1.95):
        ax.annotate("", xy=(tip * 1.09, (tip * 1.09) ** 2), xytext=(tip, tip**2),
                    arrowprops={"arrowstyle": "->", "color": SLIDE_BLUE, "lw": 2.4})
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-0.8, 5.4)

    # 3. Domain not closed: the endpoints are missing.
    ax = axes[2]
    x = np.linspace(0.0, 1.0, 50)
    ax.plot(x, x, color=SLIDE_BLUE, lw=3.0)
    for point in ((0, 0), (1, 1)):
        ax.scatter([point[0]], [point[1]], s=58, facecolor="white",
                   edgecolor=SLIDE_BLUE, linewidth=2.2, zorder=5)
    ax.set_xlim(-0.28, 1.28)
    ax.set_ylim(-0.30, 1.32)

    # 4. Compact domain but a jump exactly where the supremum would be.
    ax = axes[3]
    x = np.linspace(0.0, 1.0, 60)
    ax.plot(x, x, color=SLIDE_BLUE, lw=3.0)
    ax.scatter([1], [1], s=58, facecolor="white", edgecolor=SLIDE_BLUE,
               linewidth=2.2, zorder=6)
    ax.scatter([1], [0], s=52, color=SLIDE_BLUE, zorder=6)
    ax.scatter([0], [0], s=52, color=SLIDE_BLUE, zorder=6)
    ax.set_xlim(-0.28, 1.28)
    ax.set_ylim(-0.30, 1.32)

    panels = (
        (r"$f(x)=x^2$ on $[-1,2]$", "$D$ compact, $f$ continuous",
         "max and min attained", SLIDE_GREEN),
        (r"$f(x)=x^2$ on $\mathbb{R}$", "$D$ not bounded",
         "no maximum", SLIDE_RED),
        (r"$f(x)=x$ on $(0,1)$", "$D$ not closed",
         "neither attained", SLIDE_RED),
        (r"jump on $[0,1]$", "$f$ not continuous",
         "no maximum", SLIDE_RED),
    )
    for ax, (formula, antecedent, consequent, color) in zip(axes, panels):
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.axhline(0, color=SLIDE_GRAY, lw=0.8)
        ax.axvline(0, color=SLIDE_GRAY, lw=0.8)
        ax.set_title(formula, fontsize=18, pad=4)
        ax.text(0.5, -0.13, antecedent, color=color, fontsize=16,
                ha="center", va="top", transform=ax.transAxes)
        ax.text(0.5, -0.34, r"$\Longrightarrow$ " + consequent, color=color,
                fontsize=16, ha="center", va="top", transform=ax.transAxes)

    fig.subplots_adjust(left=0.015, right=0.985, bottom=0.26, top=0.83, wspace=0.26)
    save_vector_pair(fig, "weierstrass-failures")


def make_boundary_candidates() -> None:
    fig, ax = plt.subplots(figsize=(7.0, 3.3))
    x = np.linspace(-1.0, 2.0, 300)
    ax.plot(x, x**2, color=SLIDE_BLUE, lw=3.0)

    # Interior stationary point: the global minimum.
    ax.scatter([0], [0], s=56, color=SLIDE_RED, zorder=5)
    ax.plot([-0.34, 0.34], [0, 0], color=SLIDE_RED, lw=2.4)
    ax.text(0, -0.62, r"$x=0$: interior, $f'(0)=0$", color=SLIDE_RED,
            ha="center", va="top", fontsize=17)

    # Boundary point: the global maximum, slope nonzero.
    ax.scatter([2], [4], s=56, color=SLIDE_GREEN, zorder=5)
    segment = np.linspace(1.72, 2.05, 40)
    ax.plot(segment, 4 + 4 * (segment - 2), color=SLIDE_GREEN, lw=2.4)
    ax.text(1.96, 4.42, r"$x=2$: boundary, $f'(2)=4$", color=SLIDE_GREEN,
            ha="right", va="bottom", fontsize=17)

    ax.scatter([-1], [1], s=30, color=SLIDE_BLUE, zorder=5)
    ax.plot([2, 2], [0, 4], color=SLIDE_GRAY, lw=1.0, ls="--")
    ax.axhline(0, color=SLIDE_GRAY, lw=0.9)
    for tick, label in ((-1, "$-1$"), (2, "$2$")):
        ax.plot([tick, tick], [-0.09, 0.09], color=SLIDE_GRAY, lw=1.0)
        if tick != 2:
            ax.text(tick, -0.30, label, ha="center", va="top", fontsize=15)
    ax.text(2, -0.30, "$2$", ha="center", va="top", fontsize=15)

    ax.set_xlim(-1.45, 2.9)
    ax.set_ylim(-1.35, 5.2)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout(pad=0.15)
    save_vector_pair(fig, "boundary-candidates")


def make_kkt_regimes() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.1))
    cases = (
        (0.0, 1.45, r"slack: $h(x^*)>0$, $\lambda^*=0$", SLIDE_GREEN),
        (1.9, 0.75, r"binding: $h(x^*)=0$, $\lambda^*>0$", SLIDE_RED),
    )
    for ax, (peak, cutoff, title, color) in zip(axes, cases):
        x = np.linspace(-1.6, 2.9, 400)
        f = 4 - (x - peak) ** 2
        ax.plot(x, f, color=SLIDE_BLUE, lw=3.0)
        ax.axvspan(-1.6, cutoff, color=SLIDE_BLUE, alpha=0.07)
        ax.plot([cutoff, cutoff], [-0.4, 4.75], color=SLIDE_GRAY, lw=2.2)
        ax.text(cutoff, -0.62, "$c$", ha="center", va="top", fontsize=17)

        best = min(peak, cutoff)
        fbest = 4 - (best - peak) ** 2
        ax.scatter([best], [fbest], s=58, color=color, zorder=5)
        if best == peak:
            ax.plot([peak - 0.33, peak + 0.33], [4, 4], color=color, lw=2.4)
            ax.text(peak, -0.62, "$x^*$", ha="center", va="top", fontsize=17)
        else:
            slope = -2 * (best - peak)
            segment = np.linspace(best - 0.3, best + 0.3, 40)
            ax.plot(segment, fbest + slope * (segment - best), color=color, lw=2.4)
            ax.text(cutoff - 0.18, fbest + 0.42, "$x^*=c$", ha="right",
                    va="bottom", color=color, fontsize=17)

        ax.axhline(0, color=SLIDE_GRAY, lw=0.9)
        ax.set_xlim(-1.7, 3.0)
        ax.set_ylim(-1.35, 5.6)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_title(title, fontsize=18, pad=6, color=color)
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.14, top=0.82, wspace=0.22)
    save_vector_pair(fig, "kkt-regimes")




def make_multiplier_surface() -> None:
    """The shadow value seen on the objective surface.

    Companion to the level-set view in ``multiplier-relaxation``.  Styling
    follows the Day 3 utility surface and ``lagrange-surface``: a very
    transparent Chad Green surface, Chad Blue feasible curves, transparent
    panes and the same camera angle.  Relaxing the constraint from c to
    c + dc lifts the feasible curve, and the optimum climbs by dF.
    """
    grid = np.linspace(0, 2, 120)
    x1, x2 = np.meshgrid(grid, grid)
    objective = 4 - (x1 - 1) ** 2 - (x2 - 1) ** 2

    tight, relaxed = 0.9, 1.6          # constraint levels c and c + dc

    def optimum(level):
        point = level / 2.0
        return point, point, 4 - 2 * (point - 1) ** 2

    fig = plt.figure(figsize=(5.55, 4.25))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(
        x1, x2, objective, color=SLIDE_GREEN, alpha=0.11,
        rcount=42, ccount=42, linewidth=0, antialiased=True, shade=False,
    )

    # Both constraint planes, the relaxed one fainter.
    for level, alpha in ((tight, 0.15), (relaxed, 0.09)):
        parameter = np.linspace(max(0.0, level - 2.0), min(level, 2.0), 160)
        plane_z = np.linspace(2.05, 4.12, 2)
        plane_x1, plane_z = np.meshgrid(parameter, plane_z)
        ax.plot_surface(
            plane_x1, level - plane_x1, plane_z,
            color=SLIDE_GRAY, alpha=alpha, linewidth=0, shade=False,
        )

    # Feasible curves lifted onto the surface: tight solid and dark, the
    # relaxed one lighter and dashed so the pair never reads as one line.
    for level, style, width, tone in (
        (tight, "-", 3.2, SLIDE_BLUE),
        (relaxed, "--", 2.9, CONTOUR_COLORS[0]),
    ):
        parameter = np.linspace(max(0.0, level - 2.0), min(level, 2.0), 200)
        curve_x2 = level - parameter
        ax.plot(
            parameter, curve_x2,
            4 - (parameter - 1) ** 2 - (curve_x2 - 1) ** 2,
            color=tone, lw=width, ls=style, zorder=7,
        )

    low = optimum(tight)
    high = optimum(relaxed)

    # Guide from the tight optimum across to the relaxed one, so the red
    # segment reads as the difference between two heights.
    ax.plot(
        [low[0], high[0]], [low[1], high[1]], [low[2], low[2]],
        color=SLIDE_GRAY, lw=1.4, ls=":", zorder=9,
    )
    ax.plot(
        [high[0], high[0]], [high[1], high[1]], [low[2], high[2]],
        color=SLIDE_RED, lw=3.2, zorder=11,
    )
    ax.scatter(*low, s=54, color=SLIDE_RED, depthshade=False, zorder=12)
    ax.scatter(*high, s=54, color=SLIDE_RED, depthshade=False, zorder=12)
    ax.text(
        high[0] + 0.26, high[1] + 0.06, (low[2] + high[2]) / 2 - 0.02,
        r"$\Delta F$", color=SLIDE_RED, ha="left", fontsize=15,
    )

    # Label each feasible curve at its free end, clear of the surface.
    ax.text(0.96, 0.02, 3.00, "$c$", color=SLIDE_BLUE, ha="left", fontsize=14)
    ax.text(1.70, 0.02, 2.62, r"$c+\Delta c$", color=CONTOUR_COLORS[0],
            ha="left", fontsize=14)

    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_zlim(2, 4.18)
    ax.set_xticks([0, 1, 2])
    ax.set_yticks([0, 1, 2])
    ax.set_zticks([2, 3, 4])
    ax.set_xlabel(r"$x_1$", labelpad=4)
    ax.set_ylabel(r"$x_2$", labelpad=4)
    ax.set_zlabel(r"$f(x_1,x_2)$", labelpad=5)
    ax.view_init(elev=25, azim=-58)
    ax.set_box_aspect((1, 1, 0.82))
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1, 1, 1, 0))
        axis.pane.set_edgecolor((1, 1, 1, 0))
    ax.grid(True, alpha=0.18)
    fig.subplots_adjust(left=0.01, right=0.92, bottom=0.02, top=0.98)
    save_vector_pair(fig, "multiplier-surface")


def make_all() -> None:
    make_sundaram_global_local()
    make_sundaram_foc_signs()
    make_foc_slope()
    make_critical_points()
    make_gradient_directions()
    make_constraint_tangent()
    make_crossing_level_set()
    make_lagrange_tangency()
    make_lagrange_surface()
    make_hessian_surfaces()
    make_multiplier_relaxation()
    make_multiplier_surface()
    make_consumer_cases()
    make_leontief_kink()
    make_linear_demand()
    make_ces_demand()
    make_leontief_demand()
    make_weierstrass_failures()
    make_boundary_candidates()
    make_kkt_regimes()


if __name__ == "__main__":
    make_all()
