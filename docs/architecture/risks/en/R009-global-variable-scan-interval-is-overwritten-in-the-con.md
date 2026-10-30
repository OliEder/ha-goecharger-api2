# R9: Global variable `SCAN_INTERVAL` is overwritten in the constructor

| Field | Value |
|---|---|
| ID | R9 |
| Date recorded | 2026-10-27 |
| Category | Maintainability |
| Status | Open |
| Risk owner | not named (to be set by the maintainer) |
| Next review | with every new release |

## Risk description

If several entries with different intervals are set up, then every constructor overwrites the global variable, which means the last value set applies as the default.

## Finding in detail

**Finding.** `SCAN_INTERVAL` is a global variable that is overwritten in the constructor.

**Effect.** With several entries the last value set applies to the default. The coordinator, however, uses the interval via `update_interval=SCAN_INTERVAL` in the call right after, so mostly harmless.

## Assessment

| | W | A | Risk score | |
|---|---|---|---|---|
| Assessment | 2 | 2 | 4 | low |
| Residual risk after the countermeasure | 1 | 2 | 2 | low |

Risk strategy: **Mitigate**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.

## Countermeasure

Keep the interval per coordinator instead of globally. Proposal, not implemented.

## Status and history

Open.

## Evidence

*Evidence at the time of the finding (not today's state)*

Read from the code.  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Schluss]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../../arc42-ha-goecharger-api2.en.md) | [Back to the register](README.md)
