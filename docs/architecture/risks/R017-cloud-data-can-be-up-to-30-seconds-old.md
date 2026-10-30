---
id: R17
date: 2026-10-29
category: INT
probability: 3
impact: 2
residual_probability: 1
residual_impact: 2
strategy: mitigate
status: open
owner:
review: release
---
# R17: Cloud data can be up to 30 seconds old

## Risk description

If the integration queries the cloud `/api/status` without the parameter `age`, then the cloud returns data up to 30 seconds old, which means values in cloud polling are outdated without the integration noticing.

## Finding in detail

**Finding.** Cloud `/api/status` returns data up to 30 seconds old by default (`age=30`); the integration does not set `age`.

**Effect.** In cloud polling values can be up to 30 seconds old without the integration noticing.

## Assessment

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Assessment | 3 | 2 | 6 | medium |
| Residual risk after the countermeasure | 1 | 2 | 2 | low |

Risk strategy: **Mitigate**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.
<!-- /risk:assessment -->

## Countermeasure

Set `age` or evaluate the header `last-modified`. Proposal, not implemented.

## Status and history

<!-- risk:status -->
Open
<!-- /risk:status -->

## Evidence

*Evidence at the time of the finding (not today's state)*

Documentation and code read (no `age` in the calls).  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Inference]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../arc42-ha-goecharger-api2.md) | [Back to the register](README.md)
