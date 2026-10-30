# R23: Blueprint in `main` has no zero-value branch for invalid measurements

| Field | Value |
|---|---|
| ID | R23 |
| Date recorded | 2026-10-29 |
| Category | Integration / third party |
| Status | Open |
| Risk owner | not named (to be set by the maintainer) |
| Next review | with every new release |

## Risk description

If a sensor of the PV blueprint fails during the day, then the blueprint skips the delivery instead of sending zero values, which means the moving averages of the wallbox stand still and charging from the grid may happen unintentionally.

## Finding in detail

**Finding.** The blueprint version merged into `main` (PR #171 plus #174, built in manually by marq24) does **not** contain the extensions of the original version of PR #171: on invalid measurements the day's delivery is **skipped** (no zero value), on a wrong target selection `stop` with `error: true` every 5 seconds, `mode: single` without `max_exceeded: silent`, no battery switch, no grace period. The behaviour is stated in the blueprint text as a deliberate decision ("does not clear its previous averages").

**Effect.** If a sensor fails during the day, the moving averages of the wallbox stand still. "Send zero values" would avoid this risk.

## Assessment

| | W | A | Risk score | |
|---|---|---|---|---|
| Assessment | 3 | 3 | 9 | medium |
| Residual risk after the countermeasure | 2 | 3 | 6 | medium |

Risk strategy: **Mitigate**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.

## Countermeasure

The behaviour is described in the blueprint as a deliberate decision. An option "send zero values" would be the countermeasure. Proposal.

## Status and history

Open.

## Evidence

*Evidence at the time of the finding (not today's state)*

Source code read.  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Schluss]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../../arc42-ha-goecharger-api2.en.md) | [Back to the register](README.md)
