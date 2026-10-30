# R7: README and code state different read intervals for the configuration

| Field | Value |
|---|---|
| ID | R7 |
| Date recorded | 2026-10-27 |
| Category | Documentation |
| Status | Open |
| Risk owner | not named (to be set by the maintainer) |
| Next review | with every new release |

## Risk description

If users rely on the statement "every 24 hours" in the README, then the code already reads the configuration hourly, which means they have a wrong expectation of the load and the freshness.

## Finding in detail

**Finding.** Documentation and code differ: README "configuration every 24 hours", code hourly (`+ 3600`).

**Effect.** Wrong expectation for users.

## Assessment

| | W | A | Risk score | |
|---|---|---|---|---|
| Assessment | 5 | 1 | 5 | low |
| Residual risk after the countermeasure | 1 | 1 | 1 | low |

Risk strategy: **Mitigate**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.

## Countermeasure

Adjust the README or the interval. Proposal, not implemented.

## Status and history

Open.

## Evidence

*Evidence at the time of the finding (not today's state)*

Read from code and README.  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Schluss]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../../arc42-ha-goecharger-api2.en.md) | [Back to the register](README.md)
