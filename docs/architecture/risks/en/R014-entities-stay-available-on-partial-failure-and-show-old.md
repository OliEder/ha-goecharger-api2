# R14: Entities stay `available` on partial failure and show old values

| Field | Value |
|---|---|
| ID | R14 |
| Date recorded | 2026-10-27 |
| Category | Technology / architecture |
| Status | Open |
| Risk owner | not named (to be set by the maintainer) |
| Next review | with every new release |

## Risk description

If the device partly fails, then the data stays and the entities remain `available` as long as the last update succeeded, which means users and automations take old values for current.

## Finding in detail

**Finding.** On partial failure of the device: data stays, entities remain `available` as long as the last update succeeded.

**Effect.** The user sees old values as current.

## Assessment

| | W | A | Risk score | |
|---|---|---|---|---|
| Assessment | 3 | 3 | 9 | medium |
| Residual risk after the countermeasure | 2 | 3 | 6 | medium |

Risk strategy: **Mitigate**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.

## Countermeasure

Set availability to "unavailable" after several failed read cycles or on WebSocket loss. Proposal, not implemented; there is no test for it.

## Status and history

Open.

## Evidence

*Evidence at the time of the finding (not today's state)*

Read from the code (`available` = `last_update_success`). I did not check how a WebSocket loss affects availability.  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Schluss]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../../arc42-ha-goecharger-api2.en.md) | [Back to the register](README.md)
