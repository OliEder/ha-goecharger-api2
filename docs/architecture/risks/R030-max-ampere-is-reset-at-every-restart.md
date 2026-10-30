---
id: R030
date: 2026-10-29
category: ARCH
probability: 3
impact: 3
residual_probability: 1
residual_impact: 3
strategy: mitigate
status: fixed
owner:
review: release
---
# R030: Max Ampere is reset at every restart

## Risk description

If Home Assistant or the integration restarts, then according to the maintainer the integration resets the maximum current, which means a configured value is lost and the limit no longer applies until it is set again.

## Finding in detail

**Finding.** According to the maintainer (issue #176) the integration reset the maximum current (Max Ampere) at every restart.

**Effect.** A previously set value was lost; the limit then no longer applied until it was set again. The cause was the 16 A limiter, since changed.

## Assessment

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Assessment | 3 | 3 | 9 | medium |
| Residual risk after the countermeasure | 1 | 3 | 3 | low |

Risk strategy: **Mitigate**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.
<!-- /risk:assessment -->

## Countermeasure

Done in `4c7207c` and `98af3e0` (limiter no longer decides from the `adi` fallback alone). A test that restarts with a 32 A charger and keeps the value is still missing.

## Status and history

<!-- risk:status -->
Closed (fixed)
<!-- /risk:status -->

The cause was the 16 A limiter, which used the `adi` fallback (see [R029](R029-without-cablecurrentlimit-there-is-no-limit-to-16-a-any.md)); changed in `4c7207c` and `98af3e0`. The reporter wrote "Working ;)" on 2026-10-29. Issue #176 is still open. The limiter stays for chargers that really are limited to 16 A. Not checked on a real device by us.

## Evidence

*Evidence at the time of the finding (not today's state)*

Statement of the maintainer, **not** replayed by us and no test for it. Whether it comes from the 16 A limiter ([R029](R029-without-cablecurrentlimit-there-is-no-limit-to-16-a-any.md)) or from taking over values at start is open.  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Inference]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../arc42-ha-goecharger-api2.md) | [Back to the register](README.md)
