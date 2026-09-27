# Security and submission audit

Reviewed: 2026-09-27

Scope: `contracts/cycle_cut.py` at SHA-256 `15c543e7172753a0a72e93b151b6f3158fac7ffdcdb0cc052e239ac3a0bc0154`, direct and integration tests, review documents, and the exact StudioNet deployment in `deployments/studionet.json`.

## Findings resolved

| Finding | Resolution |
| --- | --- |
| Case-variant node labels could represent the same logical node | Node identity is now case-insensitive after trimming. |
| Oversized model edge lists were rejected only after item-by-item processing | The 36-edge limit is enforced before iterating model items. |
| Node labels needed the same prompt-injection boundary as the narrative | Both blocks are explicitly delimited and treated as untrusted data. |
| Original coverage did not exercise repeated cycles, stable tie-breaking, or all authorization paths | Direct coverage increased from 4 to 16 tests and the five-validator flow was rerun. |

## Verification results

| Gate | Result |
| --- | --- |
| GenVM lint and semantic validation | PASS |
| Strict typecheck | PASS, zero diagnostics |
| Direct invariant and negative-path tests | PASS, 16 tests |
| Independent local validators | PASS, exactly 5 validators |
| StudioNet deployment and every state-changing receipt | PASS, FINALIZED with agreeing-validator execution success |
| Latest-final sealed-state readback | PASS |
| Deployed source byte equality | PASS |
| Deployed schema method verification | PASS |
| Secrets in repository | NONE |

StudioNet contract: `0x379a0039589282Ed571Ae11AB9AdBa1B3c4d8eae`

Deployment transaction: `0x40b618041aaae96e028c80af506aca0a38aa79abd0d796b5eb697bbc5fb79f14`

Intelligent transaction: `0xbb8c4366354fa5b332afddb1f073cfd0ce567197f57c10200b9c9dc998de6bfc`

Cut transaction: `0x64cf75afdd6863c37ad5e799321503c69462117c391f3298526a1961c90efce6`

Seal transaction: `0x7da80de302fe91d5a8bf4eab2135980f03329a1c1a4b8de690237f74c392c05d`

Observed latest-final state: `{"state":"SEALED","edges":[[0,1],[1,2]],"cuts":[{"edge":[2,0]}],"order":[0,1,2]}`

## Residual trust assumptions

- Validators infer dependencies from the supplied narrative; consensus is not proof of real-world truth or completeness.
- The owner deliberately controls whether a proposed cut is accepted. That approval is recorded, not automated.
- StudioNet is a test network, not a production availability or economic-security guarantee.

No known review-blocking source, authorization, state-machine, validation, test, or provenance defect remains. This is a focused engineering audit, not a formal proof or a promise of program acceptance.
