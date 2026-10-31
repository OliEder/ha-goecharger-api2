---
id: R003
date: 2026-10-27
category: ARCH
probability: 2
impact: 3
residual_probability: 1
residual_impact: 3
strategy: mitigate
status: fixed
owner:
review: release
---
# R003: Active charger counter with controller entries

## Risk description

If a controller entry is unloaded, then the code lowers the counter `ACTIVE_CHARGER_COUNTER`, which only chargers had raised, which means the charger services disappear or a `KeyError` occurs.

## Finding in detail

**Finding.** `async_unload_entry`: `ACTIVE_CHARGER_COUNTER` is raised only for chargers but lowered for every entry and then read without protection. For a controller-only entry the key is missing.

**Effect.** Possible `KeyError` on unload or a wrong counter with mixed entries.

## Assessment

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Assessment | 2 | 3 | 6 | medium |
| Residual risk after the countermeasure | 1 | 3 | 3 | low |

Risk strategy: **Mitigate**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.
<!-- /risk:assessment -->

## Countermeasure

Counter and services are adjusted for chargers only (`eb5da46`).

## Status and history

<!-- risk:status -->
Closed (fixed)
<!-- /risk:status -->

`eb5da46`. Since `eb5da46` counter and services are adjusted for chargers only.

## Evidence

*Evidence at the time of the finding (not today's state)*

[Code] `__init__.py` lines 150 to 211. [Test] The finding is replayed by the test suite, green on `main` (`e6ee0c3`) on 2026-10-30: `test_controller_does_not_register_charger_services` (setting up a controller leaves no counter), `test_unloading_a_controller_keeps_the_charger_services` (a controller unload does not lower the counter of a loaded charger) and `test_unloading_a_controller_without_any_charger_does_not_raise`. The fakes replace platform loading, polling and the WebSocket start; the original `KeyError` was not run in a real Home Assistant.  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Inference]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../arc42-ha-goecharger-api2.md) | [Back to the register](README.md)
