# Day 5 — Revision Outline

## Audience and rhetoric

- Source: existing Beamer lecture, *General Equilibrium and the Social Planner*.
- Audience: first-year graduate economics students in a mathematics bootcamp.
- Balance: teaching lecture — formal dynamic optimization first, then equilibrium economics.
- Format: Beamer, using the established Days 1–5 visual system.
- Figures: Python-generated vector graphics in the established deck palette.
- Closing sentence: general equilibrium is optimization made mutually consistent.

## Preservation constraints

- Keep the infinite-horizon formulation, zero depreciation, prices `r_t` and `w_t`,
  the static firm problem, and standard Cobb–Douglas technology.
- Keep the mathematics-first structure, but anchor generic notation immediately in
  dated saving or next-period capital.
- Keep the path-space existence caveat and the final closing sentence.
- Use `L`, never a curly Lagrangean symbol.

## Arc

### Act I — From a point to a path

1. Title.
2. Today.
3. Day 4 chose a point; Day 5 chooses an infinite path.
4. One dated constraint requires one dated multiplier.
5. Next period's state appears in two neighboring constraints.
6. The Euler recurrence needs conditions at both ends.
7. Translate the abstract recurrence into saving and capital.
8. Treat dated consumption as different commodities.

### Act II — Household and firm optimization

9. State the primitives.
10–14. Define lifetime utility, saving, the household path problem, dated shadow values,
    and the intertemporal tangency.
15. Derive the Euler equation as marginal cost equals marginal benefit.
16. Place the transversality condition after the Euler equation and explain its role.
17–22. Define technology, the static firm problem, factor prices, feasibility, and
    the possible set-valued firm response.

### Act III — Equilibrium, characterization, and the planner

23–27. Define competitive equilibrium before deriving its clearing implications.
28–30. Build the capital recurrence as a visible three-step substitution chain and
    distinguish characterization from existence.
31–36. Define efficiency and the planner, compare Euler equations, and state the
    model-specific market–planner equivalence and decentralization result.
37. Explain why infinite-horizon existence needs a separate theorem.
38. Close with optimization made mutually consistent.

## Figure

- `intertemporal-choice.pdf`: intertemporal tangency, with directly labeled budget
  and indifference curves.
