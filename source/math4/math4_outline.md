# Day 4 — Revision Outline

## Audience and rhetoric

- Source: existing Beamer lecture, *Optimization and Economic Choice*.
- Audience: first-year graduate economics students in a mathematics bootcamp.
- Balance: teaching lecture — clarity and intuition support formal mathematics.
- Format: Beamer, using the established Days 1–5 visual system.
- Figures: Python-generated vector graphics in the established deck palette.
- Closing sentence: first-order conditions narrow the search; verification finishes it.

## Preservation constraints

- Keep the mathematics-first, economics-second architecture.
- Keep the practical Extreme Value Theorem, the proof of the scalar first-order condition,
  the formal multiplier theorem, the 3D Lagrange figure, and the consumer and firm cases.
- Do not replace the author's voice with generic presentation language.
- Improve rhythm by shortening selected titles and removing only redundant restatements.

## Arc

### Act I — What optimization asks

1. Title.
2. Today.
3. Before differentiating, separate existence from identification.
4. Distinguish the maximum value from the maximizing choices.
5. Show that the argmax may be empty, unique, or set-valued.
6. State the Extreme Value Theorem in practical terms.

### Act II — How candidates are generated and verified

7. Explain why the usual first-order condition is an interior condition.
8. Use the slope figure to show the improving direction.
9. Prove the scalar first-order condition.
10. Show why a zero derivative is not sufficient.
11. Give the local second-derivative test.
12. Use concavity to obtain a global conclusion.
13. Give the reliable closed-interval workflow.
14–20. Develop equality constraints, tangency, the Lagrangean, regularity,
    multiplier uniqueness, and sensitivity without weakening the formal layer.
21. Introduce Kuhn–Tucker through stationarity and complementary slackness.

### Act III — Apply the same mathematics to economics

22. Time for economics.
23–31. Consumer demand: existence, binding budgets, smooth interiors, corners, and kinks.
32–33. Static firm choice, including linear production and possible nonexistence.
34. Close with existence, candidates, and verification.

## Figures

- `foc-slope.pdf`: a nonzero slope leaves an improving direction.
- `lagrange-tangency.pdf`: constrained optimum as tangency.
- `lagrange-surface.pdf`: 3D objective surface and feasible curve.
