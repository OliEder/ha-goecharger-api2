# R6: No `unique_id` in the config flow

| Field | Value |
|---|---|
| ID | R6 |
| Date recorded | 2026-10-27 |
| Category | Technology / architecture |
| Status | Open |
| Risk owner | not named (to be set by the maintainer) |
| Next review | with every new release |

## Risk description

If a user sets up the same charger a second time, then `_abort_if_unique_id_configured()` does not take effect because no `unique_id` is ever set, which means duplicate entries and duplicate entities are created.

## Finding in detail

**Finding.** `_abort_if_unique_id_configured()` is called, but no `unique_id` is set anywhere in the config flow (`async_set_unique_id` does not occur).

**Effect.** No protection against devices created twice.

## Assessment

| | W | A | Risk score | |
|---|---|---|---|---|
| Assessment | 3 | 2 | 6 | medium |
| Residual risk after the countermeasure | 1 | 2 | 2 | low |

Risk strategy: **Mitigate**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.

## Countermeasure

Call `async_set_unique_id` with the serial number in the config flow. Proposal, not implemented.

## Status and history

Open.

## Evidence

*Evidence at the time of the finding (not today's state)*

Read from the code (grep). Effect not demonstrated.  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Schluss]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../../arc42-ha-goecharger-api2.en.md) | [Back to the register](README.md)
