---
Title: "A Complexity Primer — Landscapes & Search"
Source: Paraphrase (INCOSE primer + Scott E. Page)
Language: en
Tags: landscape, search, optimization, simulated-annealing
License-note: Transformative paraphrase for internal Knowledge Base use.
---

# A Complexity Primer — Landscapes & Search

## Landscapes metaphor
- The 'fitness landscape' visualizes solution quality across options: Mount-Fuji (single peak), Rugged (many local peaks), Dancing (peaks shift as agents adapt).

## Design and search implications
- Mount-Fuji: greedy/gradient search is effective.
- Rugged: require exploration strategies (simulated annealing, randomized search).
- Dancing: continuous exploration; ongoing adaptation required because optima move.

## Practical guidance
1. Diagnose landscape type before selecting search or optimization strategy.
2. Use staged exploration: more randomization early, then gradual exploitation.
3. Prefer experiments and policy rollouts over one-shot optimization on dynamic landscapes.

