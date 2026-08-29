"""Render the preview images used in README.md.

Each preview stacks two slides that belong together, so the pairing itself
carries the idea: the programming block above the proof it models, the
partition above the curves that cannot touch.

Slides are found by their title text rather than by page number, so the
previews survive edits that move a slide within its deck.  Requires
``pdftoppm`` (poppler) on PATH, and Pillow.

Usage:  python tools/make_previews.py [--dpi N] [--out DIR]

The defaults write the README images. A higher --dpi and a different
--out give the same pairings sized for sharing elsewhere.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "output" / "pdf"
OUT_DIR = ROOT / "assets" / "preview"

DPI = 220           # 1386 px wide: sharp on a retina README, still light
PAD = 70            # white kept above and below the trimmed content
GAP = 30            # gutter between the two stacked slides
RULE = 3            # hairline marking the seam
RULE_RGB = (205, 208, 214)

# (output name, [(deck, slide title), (deck, slide title)])
PREVIEWS = [
    ("classes-and-curves", [("math3", "Equivalence Classes"),
                            ("math3", "Indifference Curves")]),
    ("proofs-as-programming", [("math1", "Structured Programming"),
                               ("math1", "Proofs as Structured Programming")]),
    ("books", [("math2", "Bartle-Sherbert - Real Analysis"),
               ("math1", "MWG: Microeconomic Theory")]),
    ("utility-and-hessian", [("math3", "Utility Representation"),
                             ("math4", "The Hessian")]),
]


def page_count(pdf):
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    return int(out.split("Pages:")[1].split()[0])


def find_page(pdf, title, workdir):
    """First page whose text begins with `title`. Exact, to avoid prefix clashes."""
    want = re.sub(r"\s+", " ", title).strip().lower()
    for pg in range(1, page_count(pdf) + 1):
        stem = workdir / ("pg%d" % pg)
        subprocess.run(["pdftotext", "-f", str(pg), "-l", str(pg), str(pdf),
                        str(stem) + ".txt"], capture_output=True)
        text = (stem.with_suffix(".txt")).read_text(encoding="utf-8", errors="replace")
        head = re.sub(r"\s+", " ", text).strip().lower()
        # A title matches only if the page opens with it and the next character
        # is not a letter, so "Structured Programming" does not swallow
        # "Structured Programming and ...".
        if head.startswith(want) and not head[len(want):len(want) + 1].isalpha():
            return pg
    raise SystemExit("no slide titled %r in %s" % (title, pdf.name))


def render(pdf, page, dest_stem, workdir):
    out = workdir / dest_stem
    subprocess.run(["pdftoppm", "-png", "-r", str(DPI), "-f", str(page),
                    "-l", str(page), "-singlefile", str(pdf), str(out)], check=True)
    return Image.open(out.with_suffix(".png")).convert("RGB")


def vtrim(im, pad=PAD):
    """Trim empty space above and below. Full width is kept so titles align."""
    bg = Image.new("RGB", im.size, "white")
    mask = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 8 else 0)
    box = mask.getbbox()
    if not box:
        return im
    return im.crop((0, max(0, box[1] - pad), im.width, min(im.height, box[3] + pad)))


def stack(top, bottom):
    top, bottom = vtrim(top), vtrim(bottom)
    if top.width != bottom.width:
        bottom = bottom.resize(
            (top.width, round(bottom.height * top.width / bottom.width)), Image.LANCZOS)
    canvas = Image.new("RGB", (top.width, top.height + GAP + bottom.height), "white")
    canvas.paste(top, (0, 0))
    canvas.paste(bottom, (0, top.height + GAP))
    inset = int(top.width * 0.06)
    canvas.paste(Image.new("RGB", (top.width - 2 * inset, RULE), RULE_RGB),
                 (inset, top.height + GAP // 2 - RULE // 2))
    return canvas


def show(path):
    """Repo-relative when it is inside the repo, absolute otherwise."""
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return path


def parse_args(argv):
    import argparse
    ap = argparse.ArgumentParser(description="Build the README preview images.")
    ap.add_argument("--dpi", type=int, default=DPI,
                    help="render resolution (default %d)" % DPI)
    ap.add_argument("--out", type=Path, default=OUT_DIR,
                    help="output directory (default assets/preview)")
    return ap.parse_args(argv)


def main(argv=None):
    global DPI, OUT_DIR
    args = parse_args(argv if argv is not None else sys.argv[1:])
    DPI, OUT_DIR = args.dpi, args.out
    if not shutil.which("pdftoppm") or not shutil.which("pdftotext"):
        raise SystemExit("pdftoppm and pdftotext (poppler) are required")
    missing = [d for d, _ in {(d, t) for _, pairs in PREVIEWS for d, t in pairs}
               if not (PDF_DIR / (d + ".pdf")).exists()]
    if missing:
        raise SystemExit("build the decks first (./build.sh): missing %s"
                         % ", ".join(sorted(set(missing))))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        for name, pair in PREVIEWS:
            images = []
            for i, (deck, title) in enumerate(pair):
                pdf = PDF_DIR / (deck + ".pdf")
                page = find_page(pdf, title, work)
                images.append(render(pdf, page, "%s-%d" % (name, i), work))
                print("  %-22s %s p%d  %s" % (name, deck, page, title))
            out = OUT_DIR / (name + ".png")
            stack(*images).save(out, "PNG", optimize=True)
            print("  -> %s  (%.1f MB)" % (show(out),
                                          out.stat().st_size / 1048576))
    print("previews written to %s" % show(OUT_DIR))


if __name__ == "__main__":
    sys.exit(main())
