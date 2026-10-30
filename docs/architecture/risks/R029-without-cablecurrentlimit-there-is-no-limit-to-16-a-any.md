---
id: R029
date: 2026-10-29
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
# R029: Without `cableCurrentLimit` there is no limit to 16 A any more

## Risk description

If `cll` has content but no `cableCurrentLimit`, then since `98af3e0` the integration sets no 16 A limit and does not check `adi`, which means sliders allow higher values although an adapter might be attached.

## Finding in detail

**Finding.** `98af3e0`: if `cableCurrentLimit` is missing in `cll`, there is no longer a limit to 16 A and `adi` is no longer checked; Core devices without the key were limited to be safe before.

**What the keys mean.** [Inference] `cableCurrentLimit` has the same value as `cbl` ("cable_current_limit") and is the limit of the charging cable to the car. The adapter on the grid side (CEE, Schuko) has its own field `adapterCurrentLimit` in `cll` and the flag `adi`. The integration reads the whole `cll` object and the `cll` sensor shows every field, so `adapterCurrentLimit` is visible. The 16 A decision in `read_versions` (`__init__.py`, lines 755 to 787) uses `cableCurrentLimit` first and `adi` only when `cll` is empty or missing; `adapterCurrentLimit` is not part of that decision. Whether it should be is for the maintainer to decide; this is not claimed to be a defect.

**Effect.** Sliders allow higher values. According to the manual of the Gemini flex the charger reduces the current to 16 A by itself, but only with original go-e adapters (page 5); that this holds for every model is not proven. The assumption "only Flex has the key" is disproved for one device: a `go-eCharger_V4` with firmware 59.4 delivers `cableCurrentLimit` (20), see Evidence.

## Assessment

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Assessment | 3 | 2 | 6 | medium |
| Residual risk after the countermeasure | 2 | 2 | 4 | low |

Risk strategy: **Mitigate**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.
<!-- /risk:assessment -->

## Countermeasure

Check read-only on more chargers which model and firmware deliver `cableCurrentLimit` (one V4 with 59.4 does, the V5 in #176 does not). Ask the maintainer whether `adapterCurrentLimit` should take part in the 16 A decision; that would be a change in the integration code and is not ours to make. The charger limiting the current itself (with original adapters) reduces the impact.

## Status and history

<!-- risk:status -->
Open
<!-- /risk:status -->

## Evidence

*Evidence at the time of the finding (not today's state)*

Read from the diff, behaviour recorded in a test.

Added 2026-10-30, raw answer of a real device (read-only request, run by Claude for Oliver; also posted in [Discussion #184](https://github.com/marq24/ha-goecharger-api2/discussions/184#discussioncomment-19297118)): `go-eCharger_V4`, `var` 11, firmware 59.4, `cll` = `{"adapterCurrentLimit":16,"cableCurrentLimit":20,"currentLimitMax":16,"requestedCurrent":16,"temperatureCurrentLimit":32,"unsymetryCurrentLimit":32}`, `adi` true, `cbl` 20. Not known: the cable that was plugged in and whether a car was connected. One device, one moment. The assessment is unchanged: the V5 of #176 shows that the case without the key exists.

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Inference]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../arc42-ha-goecharger-api2.md) | [Back to the register](README.md)
