"""The one palette used by every slide and every figure.

`slides_header.tex` reads the generated `palette.tex`; the figure scripts
import the tuples below. Change a colour here and run

    python tools/make_palette.py && ./build.sh

to push it through both the LaTeX decks and the matplotlib figures.

Contrast ratios are against white, for text set at the size we actually use
it. WCAG asks 4.5:1 for body text and 3:1 for large or bold text.
"""

PALETTE = {
    # name        hex        contrast   used for
    "slideblue":  "#191998",  # 12.9:1  frame titles, block titles, curves
    "slidered":   "#B93333",  #  5.9:1  the thing that fails, improving moves
    "slidegray":  "#686868",  #  5.6:1  axes, constraints, neutral annotation
    "slidegreen": "#15794B",  #  5.4:1  the thing that holds, optima
    "slidegold":  "#A8690F",  #  4.5:1  a fourth accent, used sparingly
}


def as_rgb(name: str) -> tuple[float, float, float]:
    """Matplotlib wants 0-1 floats, not hex."""
    value = PALETTE[name].lstrip("#")
    return tuple(int(value[i:i + 2], 16) / 255 for i in (0, 2, 4))


SLIDE_BLUE = as_rgb("slideblue")
SLIDE_RED = as_rgb("slidered")
SLIDE_GRAY = as_rgb("slidegray")
SLIDE_GREEN = as_rgb("slidegreen")
SLIDE_GOLD = as_rgb("slidegold")
