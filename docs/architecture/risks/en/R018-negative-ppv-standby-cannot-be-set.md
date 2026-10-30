---
id: R18
date: 2026-10-29
category: INT
probability: 2
impact: 1
residual_probability: 2
residual_impact: 1
strategy: accept
status: open
owner:
review: release
---
# R18: Negative `ppv` (standby) cannot be set

## Risk description

If a user wants to report the standby state of the PV system via `set_pv_data`, then the UI limits `ppv` to values from 0, which means `pPv < 0` (standby) cannot be sent.

## Finding in detail

**Finding.** Officially `pPv < 0` means "standby", the service `set_pv_data` limits `ppv` in the UI to values from 0.

**Effect.** Standby cannot be set through the UI. Whether this is intended is unclear.

## Assessment

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Assessment | 2 | 1 | 2 | low |
| Residual risk after the countermeasure | 2 | 1 | 2 | low |

Risk strategy: **Accept**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.
<!-- /risk:assessment -->

## Countermeasure

Accepted until the maintainer clarifies whether this is intended.

## Status and history

<!-- risk:status -->
Open
<!-- /risk:status -->

## Evidence

*Evidence at the time of the finding (not today's state)*

Documentation and `services.yaml` read.  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Schluss]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../../arc42-ha-goecharger-api2.en.md) | [Back to the register](README.md)
