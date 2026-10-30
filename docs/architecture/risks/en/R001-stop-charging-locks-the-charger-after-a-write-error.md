# R1: stop_charging locks the charger after a write error

| Field | Value |
|---|---|
| ID | R1 |
| Date recorded | 2026-10-27 |
| Category | Technology / architecture |
| Status | Closed (fixed) |
| Risk owner | not named (to be set by the maintainer) |
| Next review | with every new release |

## Risk description

If the service `stop_charging` is called in WebSocket mode and the first write (`frc=1`) or the second one (`frc=0`) fails, then the charger stays locked and the flag `_stop_in_progress` stays set, which means the user cannot charge any more and further stop requests are rejected with "already in progress".

## Finding in detail

**Finding.** `stop_charging` in WebSocket mode: `write_value_to_key` returns `None`, then `Tag.FRC.key in resp` raises `TypeError`; only `ValueError` is caught. `frc=1` is set, `frc=0` is never sent, `_stop_in_progress` stays `True`.

**Effect.** The charger stays locked until someone resets `frc` by hand.

## Assessment

| | W | A | Risk score | |
|---|---|---|---|---|
| Assessment | 3 | 4 | 12 | medium |
| Residual risk after the countermeasure | 1 | 4 | 4 | low |

Risk strategy: **Mitigate**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.

## Countermeasure

A `finally` always resets the flag, both writes require an acknowledgement (`require_ack`). Done in `03b0fc3`, `9e7d62a` and `d876dfd`.

## Status and history

Closed (fixed) – `03b0fc3`, `9e7d62a`. The `TypeError` in WebSocket mode is gone (`write_value_to_key` returns `{key: value}`), `_stop_in_progress` is reset in a `finally` since `9e7d62a`. Both tests are green.

## Evidence

*Evidence at the time of the finding (not today's state)*

Replayed in a test. **Not** checked on a real device. Still in `main`.  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Schluss]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../../arc42-ha-goecharger-api2.en.md) | [Back to the register](README.md)
