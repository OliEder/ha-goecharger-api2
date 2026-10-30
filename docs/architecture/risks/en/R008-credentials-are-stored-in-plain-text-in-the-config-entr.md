---
id: R8
date: 2026-10-27
category: SEC
probability: 2
impact: 3
residual_probability: 2
residual_impact: 3
strategy: accept
status: note
owner:
review: release
---
# R8: Credentials are stored in plain text in the config entry

## Risk description

If someone gets access to the HA configuration or a backup, then password and cloud token are readable in plain text, which means they can control the device or the cloud account.

## Finding in detail

**Finding.** Credentials are in plain text in the config entry (property of Home Assistant). Further details are deliberately not listed.

**Effect.** –

## Assessment

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Assessment | 2 | 3 | 6 | medium |
| Residual risk after the countermeasure | 2 | 3 | 6 | medium |

Risk strategy: **Accept**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.
<!-- /risk:assessment -->

## Countermeasure

Home Assistant provides no vault; the risk is accepted and lies with Home Assistant. Further observations were passed to the maintainer directly and are deliberately not listed here.

## Status and history

<!-- risk:status -->
Accepted (note)
<!-- /risk:status -->

## Evidence

*Evidence at the time of the finding (not today's state)*

–  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Schluss]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../../arc42-ha-goecharger-api2.en.md) | [Back to the register](README.md)
