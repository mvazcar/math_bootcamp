#!/usr/bin/env bash
# Rebuild the whole course: figures first, then every deck.
#
#   ./build.sh          rebuild everything
#   ./build.sh math4    rebuild one deck
#
# Requires: pdflatex + latexmk (TeX Live / TinyTeX) and python with matplotlib.
set -u
cd "$(dirname "$0")"
DECKS=${1:-"math1 math2 math3 math4 math5 proofs three-proofs mwg1-questions mwg1-solutions"}
mkdir -p output/pdf
fail=0
for d in $DECKS; do
    src="source/$d"
    [ -d "$src" ] || { echo "!! no such deck: $d"; fail=1; continue; }

    # 1. regenerate this deck's figures, if it has a script
    if [ -f "$src/regenerate_vector_plots.py" ]; then
        ( cd "$src" && python regenerate_vector_plots.py ) >/dev/null 2>&1 \
            || { echo "!! $d: figure generation failed"; fail=1; }
    fi

    # 2. compile. Remove any previous output first, so a failed build can
    #    never leave a stale PDF behind that looks like a success.
    rm -f "$src/main.pdf"
    if ( cd "$src" && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex ) >/dev/null 2>&1        && [ -f "$src/main.pdf" ]; then
        cp "$src/main.pdf" "output/pdf/$d.pdf"
        pages=$(pdfinfo "output/pdf/$d.pdf" 2>/dev/null | awk '/^Pages/{print $2}')
        over=$(grep -c 'Overfull .[vh]box' "$src/main.log" 2>/dev/null); over=${over:-0}
        printf "%-8s %3s pages   %s overfull\n" "$d" "${pages:-?}" "$over"
    else
        echo "!! $d: build FAILED (see $src/main.log)"; fail=1
    fi
done
exit $fail
