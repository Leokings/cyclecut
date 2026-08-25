Project name: CycleCut

Category: Intelligent Contracts

Batch: A

One-line description: Semantic dependency cycle cutting.

What it does: Consensus derives directed dependencies; deterministic cycle detection exposes one concrete feedback edge at a time until a topological order can be sealed.

Why GenLayer: GenLayer consensus performs the bounded semantic step, then deterministic contract code executes and stores the mechanism-specific result.

Reusable: Yes. One deployment supports many independently keyed records and callers; the live fixture is only an example.

Repository: Standalone local repository. No GitHub remote is configured and nothing was pushed.

Contract source: contracts/cycle_cut.py

Source SHA-256: e3f911fee1277bc92736b4621b5b00bb6a1b1ce450d53f0ae91045f6f52dbef1

StudioNet contract: https://explorer-studio.genlayer.com/address/0xeb00EEb22C7cAaF1A7B056fBbC0aCDef8F4da2C2

Deployment transaction: https://explorer-studio.genlayer.com/tx/0xb81ca69509e213de880e22eddda9dbaa7edb541d35abcc0b822a7839ba70f9d7

Intelligent transaction: https://explorer-studio.genlayer.com/tx/0x42c7190bf0cb432824905aa9e1241032a80722f30ac2e1d27018dab81117be00

Verification: GenVM lint PASS; strict typecheck PASS; 4 direct tests PASS; five-validator GLSim PASS; finalized StudioNet intelligent write and latest-final readback PASS; exact deployed-source and schema verification PASS.

Originality: Compared with 161 workspace contract sources. Nearest pre-existing structural score is 0.180883; mechanism and source hash are distinct.

Data boundary: Caller-supplied public data only. No external source fetching, funds, identity attestation, legal effect, or private-data guarantee.
