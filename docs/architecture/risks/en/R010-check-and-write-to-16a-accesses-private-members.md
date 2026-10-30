# R10: `check_and_write_to_16a` accesses private members

| Field | Value |
|---|---|
| ID | R10 |
| Date recorded | 2026-10-27 |
| Category | Maintainability |
| Status | Open |
| Risk owner | not named (to be set by the maintainer) |
| Next review | with every new release |

## Risk description

If the bridge is restructured internally, then `check_and_write_to_16a` breaks because, as a module-level function, it calls the private method `bridge._read_filtered_data`, which means the 16 A limiter silently fails.

## Finding in detail

**Finding.** `check_and_write_to_16a`: function with `@staticmethod` at module level, also private access to `bridge._read_filtered_data`.

**Effect.** Maintainability.

## Assessment

| | W | A | Risk score | |
|---|---|---|---|---|
| Assessment | 3 | 1 | 3 | low |
| Residual risk after the countermeasure | 1 | 1 | 1 | low |

Risk strategy: **Mitigate**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.

## Countermeasure

Move the function into the coordinator and use a public bridge method. Proposal, not implemented.

## Status and history

Open.

## Evidence

*Evidence at the time of the finding (not today's state)*

Read from the code.  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Schluss]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../../arc42-ha-goecharger-api2.en.md) | [Back to the register](README.md)
