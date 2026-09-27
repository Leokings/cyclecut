# Security

## Controls

- concrete GenVM runner and Python dependencies are pinned;
- node, edge, key, narrative, and reason sizes are bounded;
- node identity is case-insensitive and duplicate-safe;
- model output has an exact closed JSON schema and bounded endpoints;
- every nondeterministic execution has an independent validator function;
- stored edges are deterministically sorted;
- only the creating wallet may approve cuts or seal an order;
- cyclic graphs cannot be sealed;
- all deployed source bytes and required schema methods are checked against StudioNet.

## Threat boundary

Node labels and narrative text are untrusted and explicitly delimited in the prompt. Prompt hardening reduces instruction-injection risk, while the output normalizer remains the authoritative boundary.

The owner can supply incomplete or misleading planning text and can decline a suggested cut. Validator consensus does not authenticate the text. No funds are held, so liveness failures lock no assets.

## Public-data warning

All calldata and stored data are public. Do not include secrets, personal data, or confidential planning material.
