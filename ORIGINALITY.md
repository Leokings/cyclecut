# Originality audit

The final source was compared against 161 GenLayer
contract sources in the workspace. All twenty new target contracts were excluded
from the pre-existing comparison pool.

Nearest pre-existing source: `returnpath\contracts\return_custody_route.py`

Combined structural score: `0.180883`

Token score: `0.294178`

AST score: `0.096553`

Nearest contract in this new set: `conflictcolor\contracts\conflict_color.py` with combined
score `0.39903`. That score reflects shared safe GenLayer
boilerplate. The mechanisms differ materially:

- This repository: Consensus derives directed dependencies; deterministic cycle detection exposes one concrete feedback edge at a time until a topological order can be sealed.
- Other repository: Consensus derives pairwise incompatibilities; deterministic greedy coloring assigns the first available lane and reports overflow without changing the semantic graph.

The two do not share the same semantic input, deterministic algorithm, storage
record, state lifecycle, or decision views. Exact source SHA-256 values are also
unique across all twenty repositories. The complete machine-readable reports are
`review-tools/twenty-originality-audit.json` and
`review-tools/twenty-pairwise-audit.json` at the workspace level.

Similarity scoring is a review aid, not a guarantee of a human review outcome.
