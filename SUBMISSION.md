Project name: CycleCut

Category: Intelligent Contracts

One-line description: Consensus dependency inference with deterministic cycle cutting and topological sealing.

What it does: GenLayer validators infer a bounded dependency graph from public planning text. Contract code deterministically detects a feedback edge, records each owner-approved cut, and seals a stable topological order.

Why GenLayer: The dependency meaning is semantic; cycle detection, authorization, validation, and ordering remain deterministic on-chain.

Repository: https://github.com/Leokings/cyclecut

Contract source: `contracts/cycle_cut.py`

Source SHA-256: `15c543e7172753a0a72e93b151b6f3158fac7ffdcdb0cc052e239ac3a0bc0154`

StudioNet contract: https://explorer-studio.genlayer.com/address/0x379a0039589282Ed571Ae11AB9AdBa1B3c4d8eae

Deployment transaction: https://explorer-studio.genlayer.com/tx/0x40b618041aaae96e028c80af506aca0a38aa79abd0d796b5eb697bbc5fb79f14

Intelligent transaction: https://explorer-studio.genlayer.com/tx/0xbb8c4366354fa5b332afddb1f073cfd0ce567197f57c10200b9c9dc998de6bfc

Verification: lint PASS; strict typecheck PASS; 16 direct tests PASS; five-validator integration PASS; complete finalized StudioNet infer/cut/seal flow PASS; latest-final readback PASS; deployed-source and schema equality PASS.

Data boundary: Public caller-supplied text only. No source authentication, funds, private-data guarantee, or legal effect.
