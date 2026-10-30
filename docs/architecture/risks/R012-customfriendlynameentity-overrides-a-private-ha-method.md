---
id: R012
date: 2026-10-27
category: INT
probability: 3
impact: 2
residual_probability: 2
residual_impact: 2
strategy: mitigate
status: open
owner:
review: release
---
# R012: `CustomFriendlyNameEntity` overrides a private HA method

## Risk description

If Home Assistant changes the private method `_Entity__async_calculate_state`, then the override misses or raises an error, which means display names are wrong or entities fail.

## Finding in detail

**Finding.** `CustomFriendlyNameEntity` overrides a private HA method.

**Effect.** Breaks with HA changes.

## Assessment

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Assessment | 3 | 2 | 6 | medium |
| Residual risk after the countermeasure | 2 | 2 | 4 | low |

Risk strategy: **Mitigate**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.
<!-- /risk:assessment -->

## Countermeasure

Run the tests against new Home Assistant versions to see breaks early (the version of the test framework is set in `requirements_dev.txt`). The override has no safeguard of its own.

## Status and history

<!-- risk:status -->
Open
<!-- /risk:status -->

## Evidence

*Evidence at the time of the finding (not today's state)*

Read from the code.  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Inference]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../arc42-ha-goecharger-api2.md) | [Back to the register](README.md)
