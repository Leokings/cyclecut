# CycleCut

CycleCut is a reusable GenLayer Intelligent Contract that turns a public planning narrative into a bounded dependency graph, detects cycles deterministically, proposes one concrete feedback edge at a time, and seals a stable topological order after the owner approves the cuts.

## How it works

1. `infer_map` validates 2–10 unique node labels and a bounded narrative, then asks GenLayer validators to infer directed edges.
2. Contract code normalizes the exact JSON shape, rejects invalid or duplicate edges, sorts the graph, and deterministically finds a back edge.
3. `cut_suggested` lets only the map owner approve the contract's current feedback-edge proposal with a public reason. The contract repeats cycle detection after every cut.
4. `seal_order` uses deterministic Kahn topological sorting with node-index tie-breaking and makes the final order immutable.

The LLM performs only bounded semantic extraction. Validation, cycle detection, cut selection, authorization, state transitions, and ordering are deterministic contract code.

## Public interface

Write methods: `infer_map`, `cut_suggested`, `seal_order`

View methods: `get_map`, `next_cut`, `is_sealed_order`

## Verification

```text
pip install -r requirements.txt
genvm-lint check contracts/cycle_cut.py
genvm-lint typecheck contracts/cycle_cut.py --strict
pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5
pytest tests/integration/test_cycle_cut_consensus.py -q
```

Verified results on 2026-09-27: lint PASS, strict typecheck PASS, 16 direct tests PASS, one five-validator integration flow PASS, and a complete StudioNet flow PASS.

StudioNet contract: https://explorer-studio.genlayer.com/address/0x379a0039589282Ed571Ae11AB9AdBa1B3c4d8eae

The finalized live flow inferred `[[0,1],[1,2],[2,0]]`, proposed and removed `[2,0]`, and sealed order `[0,1,2]`. See `deployments/studionet.json` for every transaction and the byte-for-byte source proof.

## Boundary

All labels, narratives, reasons, calldata, and stored results are public. Consensus interprets caller-supplied text; it does not prove that the narrative is complete or true. The contract moves no funds and does not provide identity, provenance, legal, or professional guarantees.
