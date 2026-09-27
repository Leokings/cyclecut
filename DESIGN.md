# Design

## Mechanism

CycleCut combines consensus-based semantic edge inference with deterministic graph processing. Validator output is useful only after it passes a closed schema: exactly one `edges` field, integer pairs only, valid non-self endpoints, no duplicates, and at most 36 edges.

Edges are sorted before storage. Depth-first coloring selects a reproducible back edge for the next cut. Once no cycle remains, Kahn's algorithm emits a reproducible topological order using the original node index as the tie-breaker.

## State machine

`infer_map` creates either `CYCLIC` or `READY`. Each owner-authorized `cut_suggested` transition remains `CYCLIC` or becomes `READY`. Only `READY` can transition to immutable `SEALED` through `seal_order`.

## On-chain responsibilities

- bound and normalize public inputs;
- reach validator consensus on semantic dependencies;
- reject malformed model output;
- detect cycles and propose deterministic cuts;
- enforce owner-only mutation;
- store cut reasons and seal a deterministic order.

## Off-chain responsibilities

Interfaces, private drafting, source provenance, notifications, graph visualization, and decisions that rely on the final order remain off-chain.
