# R15: Cloud documentation names HTTP 202 for `/api/set`

| Field | Value |
|---|---|
| ID | R15 |
| Date recorded | 2026-10-29 |
| Category | Integration / third party |
| Status | Closed (settled, not a defect) |
| Risk owner | not named (to be set by the maintainer) |
| Next review | with every new release |

## Risk description

If the cloud answered `/api/set` with 202 instead of 200, then the code would treat the success as an error, which would mean write commands in cloud polling are logged as failed.

## Finding in detail

**Finding.** According to the cloud documentation `/api/set` answers with **HTTP 202** on success. `_write_values_int` evaluates only `200` (and `500` with content), everything else counts as an error (`failed with http-status …`, return `{}`).

**Effect.** If the cloud really sends 202, write commands in cloud polling would be logged as errors despite success, and `handle_write_result` reports "could not write". On the WebSocket path this is not affected.

## Assessment

| | W | A | Risk score | |
|---|---|---|---|---|
| Assessment | 2 | 3 | 6 | medium |
| Residual risk after the countermeasure | 1 | 1 | 1 | low |

Risk strategy: **Accept**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.

## Countermeasure

None. The maintainer confirmed on 2026-10-29 in issue #172 that the real cloud answers 200 and the documentation is wrong. The test expects 200.

## Status and history

Closed (settled, not a defect) – Maintainer, Issue #172.

## Evidence

*Evidence at the time of the finding (not today's state)*

Documentation and code read. **Settled on 2026-10-29 by the maintainer (issue #172): the cloud answers with HTTP 200, the documentation is wrong. Not a defect in the code.** Not checked by us against the real cloud.  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Schluss]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../../arc42-ha-goecharger-api2.en.md) | [Back to the register](README.md)
