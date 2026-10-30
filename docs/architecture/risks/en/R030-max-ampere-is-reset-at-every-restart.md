# R30: Max Ampere is reset at every restart

| Field | Value |
|---|---|
| ID | R30 |
| Date recorded | 2026-10-29 |
| Category | Technology / architecture |
| Status | Open |
| Risk owner | not named (to be set by the maintainer) |
| Next review | with every new release |

## Risk description

If Home Assistant or the integration restarts, then according to the maintainer the integration resets the maximum current, which means a configured value is lost and the limit no longer applies until it is set again.

## Finding in detail

**Finding.** According to the maintainer (issue #176) the integration resets the maximum current (Max Ampere) at every restart.

**Effect.** A previously set value is lost; the limit then no longer applies until it is set again.

## Assessment

| | W | A | Risk score | |
|---|---|---|---|---|
| Assessment | 3 | 3 | 9 | medium |
| Residual risk after the countermeasure | 1 | 3 | 3 | low |

Risk strategy: **Mitigate**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.

## Countermeasure

Reproduce the behaviour and record it in a test; then clarify the cause (16 A limiter or taking over values at start). Statement of the maintainer, not replayed by us.

## Status and history

Open.

## Evidence

*Evidence at the time of the finding (not today's state)*

Statement of the maintainer, **not** replayed by us and no test for it. Whether it comes from the 16 A limiter (R29) or from taking over values at start is open.  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Schluss]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../../arc42-ha-goecharger-api2.en.md) | [Back to the register](README.md)
