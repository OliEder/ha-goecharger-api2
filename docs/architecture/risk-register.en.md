# Risk register: `ha-goecharger-api2`

All known risks and technical debt of the integration, one entry per finding. The register belongs to the [arc42 documentation](arc42-ha-goecharger-api2.en.md) (chapter 11) and is the source for the state of the risks. German is the source, the English version is [`risk-register.en.md`](risk-register.en.md) (this file); both are maintained together.

| | |
|---|---|
| **State** | 2026-10-30, `main` at `e6ee0c3` |
| **Origin** | A comparison of code, documentation and tests, written with AI assistance (Claude Code) and reviewed by a human. None of it was checked on a real charger unless explicitly noted. |

## Status

| Status | Meaning |
|---|---|
| open | The finding exists on `main` |
| fixed | Fixed on `main`, the column "Fixed in" names the change |
| settled (not a defect) | The maintainer has clarified that it is not a defect |
| superseded | The finding no longer applies |
| note | Not a defect, only a constraint |

## Register

The column "Evidence" describes the finding **at the time it was found**; phrases like "still in `main`" apply to that point in time. The current state is in the column "Status".

| ID | Finding | Effect | Status | Fixed in / remark | Evidence |
|---|---|---|---|---|---|
| R1 | `stop_charging` in WebSocket mode: `write_value_to_key` returns `None`, then `Tag.FRC.key in resp` raises `TypeError`; only `ValueError` is caught. `frc=1` is set, `frc=0` is never sent, `_stop_in_progress` stays `True`. | The charger stays locked until someone resets `frc` by hand. | fixed | `03b0fc3`, `9e7d62a`. The `TypeError` in WebSocket mode is gone (`write_value_to_key` returns `{key: value}`), `_stop_in_progress` is reset in a `finally` since `9e7d62a`. Both tests are green. | Replayed in a test. **Not** checked on a real device. Still in `main`.  |
| R2 | Multi-charger: the registry `_COORDINATOR_PER_CONFIGENTRYID_MAP` is filled only in the constructor of `GoeChargerApiV2Service`. The constructor runs only if the service is not yet registered, so only for the first charger. A second charger is missing from the registry, `configid=<second>` leads to `KeyError`. If the first entry is unloaded, its coordinator stays in the registry. | The documented multi-charger operation via `configid` does not work for the second charger. | fixed | `03b0fc3`, ADR-0010 (`4702213`). The registry is maintained for every charger, reloading replaces the old coordinator. The changing default charger has been decided through ADR-0010 since `4702213` (no default with several chargers). | Read from the code (`service.py:17,33,41`, `__init__.py:153`ff). **Not replayed.**  |
| R3 | `async_unload_entry`: `ACTIVE_CHARGER_COUNTER` is raised only for chargers but lowered for every entry and then read without protection. For a controller-only entry the key is missing. | Possible `KeyError` on unload or a wrong counter with mixed entries. | fixed | `eb5da46`. Since `eb5da46` counter and services are adjusted for chargers only. | Read from the code (`__init__.py:148`ff, `194`ff). **Not replayed.**  |
| R4 | `async_write_multiple_keys`: `_handle_client_connection_error` is called with one argument instead of two (`__init__.py:674`). | `TypeError` instead of clean error handling when the connection drops during writing (affects the vehicle selection `ct`). | fixed | `03b0fc3`. The call now has two arguments. | Replayed in a test. Still in `main`.  |
| R5 | `set_pv_data` checks `pgrid` only with `isinstance(Number)` (`service.py:59`), but `ppv` and `pakku` for finiteness. | `NaN` or `inf` as `pgrid` can go to the charger as invalid JSON. | fixed | `eb5da46`. Since `eb5da46` `set_pv_data` also checks `pgrid` for finiteness. | Read from the code. Low practical relevance because the blueprint checks.  |
| R6 | `_abort_if_unique_id_configured()` is called, but no `unique_id` is set anywhere in the config flow (`async_set_unique_id` does not occur). | No protection against devices created twice. | open |  | Read from the code (grep). Effect not demonstrated.  |
| R7 | Documentation and code differ: README "configuration every 24 hours", code hourly (`+ 3600`). | Wrong expectation for users. | open |  | Read from code and README.  |
| R8 | Credentials are in plain text in the config entry (property of Home Assistant). Further details are deliberately not listed. | – | note |  | –  |
| R9 | `SCAN_INTERVAL` is a global variable that is overwritten in the constructor. | With several entries the last value set applies to the default. The coordinator, however, uses the interval via `update_interval=SCAN_INTERVAL` in the call right after, so mostly harmless. | open |  | Read from the code.  |
| R10 | `check_and_write_to_16a`: function with `@staticmethod` at module level, also private access to `bridge._read_filtered_data`. | Maintainability. | open |  | Read from the code.  |
| R11 | Missing dependency in the manifest (`bcrypt`), minimum HA version unclear (`hacs.json` 2023.8.0 versus newer APIs used). | Installation errors on older systems possible. | open |  | Read from code and manifest. I did not check whether `bcrypt` is supplied by HA.  |
| R12 | `CustomFriendlyNameEntity` overrides a private HA method. | Breaks with HA changes. | open |  | Read from the code.  |
| R13 | No tests in the repo (superseded: since PR #178 they are in `tests/integration`). | Regressions are found only by users. | superseded | PR #178, #179. | Repo content.  |
| R14 | On partial failure of the device: data stays, entities remain `available` as long as the last update succeeded. | The user sees old values as current. | open |  | Read from the code (`available` = `last_update_success`). I did not check how a WebSocket loss affects availability.  |
| R15 | According to the cloud documentation `/api/set` answers with **HTTP 202** on success. `_write_values_int` evaluates only `200` (and `500` with content), everything else counts as an error (`failed with http-status …`, return `{}`). | If the cloud really sends 202, write commands in cloud polling would be logged as errors despite success, and `handle_write_result` reports "could not write". On the WebSocket path this is not affected. | settled (not a defect) | Maintainer, Issue #172. | Documentation and code read. **Settled on 2026-10-29 by the maintainer (issue #172): the cloud answers with HTTP 200, the documentation is wrong. Not a defect in the code.** Not checked by us against the real cloud.  |
| R16 | The preferred data path (WebSocket) is not officially documented; login procedure and messages are reverse engineered. | A firmware or cloud change by go-e can break it without warning. The README already mentions this for firmware 60.2 and 60.4. | open |  | Documentation and README read.  |
| R17 | Cloud `/api/status` returns data up to 30 seconds old by default (`age=30`); the integration does not set `age`. | In cloud polling values can be up to 30 seconds old without the integration noticing. | open |  | Documentation and code read (no `age` in the calls).  |
| R18 | Officially `pPv < 0` means "standby", the service `set_pv_data` limits `ppv` in the UI to values from 0. | Standby cannot be set through the UI. Whether this is intended is unclear. | open |  | Documentation and `services.yaml` read.  |
| R19 | Officially the cloud token is readable via the key `cak` (so also via the local API, as far as the key is available there). | A measure of the integration to protect the token only in the config entry would then be only partly effective. I did not check whether `cak` is really readable locally without login. | open |  | Documentation only read.  |
| R20 | Since `5328e74`, `read_all_states`, `read_all_config` and `read_versions` overwrite the stored state only if the answer is not empty (`if ret is not None and len(ret) > 0 …`). Before, the state was cleared on an error. `_read_filtered_data` returns `{}` for every status except 200/400 (for example cloud 403 or 404 when offline). | The coordinator keeps the last values and reports success. A charger that went offline keeps showing its last values in cloud mode. In addition `_async_update_data` resets the error counter because the `ChainMap` of the old values is not empty. | open |  | Derived from diff and code, **not tested**. Whether the display really stays "frozen" depends on what HA does with an unchanged `last_update_success`.  |
| R21 | The migration from 2.0 to 2.1 deletes **all devices** of the entry (`async_remove_device`). To my knowledge HA thereby also removes the related entries of the entity registry. | Names, areas, labels and manually enabled entities (many sensors are off by default) adjusted by users are probably lost and must be set again. The entity IDs stay the same because they are generated in the code. | open |  | HA behaviour from memory, in the code only the call is proven. **Not replayed.**  |
| R22 | Entries with version 1 are migrated directly to 2.1 and skip deleting the devices. The old clean-up function `check_device_registry` was removed. | Old devices with the earlier identifier (which contained the token for cloud entries) stay in the registry there. Very rare edge case. | open |  | Read from the diff.  |
| R23 | The blueprint version merged into `main` (PR #171 plus #174, built in manually by marq24) does **not** contain the extensions of the original version of PR #171: on invalid measurements the day's delivery is **skipped** (no zero value), on a wrong target selection `stop` with `error: true` every 5 seconds, `mode: single` without `max_exceeded: silent`, no battery switch, no grace period. The behaviour is stated in the blueprint text as a deliberate decision ("does not clear its previous averages"). | If a sensor fails during the day, the moving averages of the wallbox stand still. "Send zero values" would avoid this risk. | open |  | Source code read.  |
| R24 | `_write_values_int` checks the answer of the charger for the key only for "true". According to `http-en.md` the value can be `true` or an **error text**. The code treats a text as success. | Rejections by the charger (also for `ids`) would be reported as success. | fixed | (commit not traced). The test `test_write_rejected_by_charger_returns_err` is green on `9e7d62a`; I did not trace when exactly the answer with an error text is evaluated. | Derived from code and documentation, shown in a test with a fake (`known_bug`). **Not** checked on a device.  |
| R25 | `async_setup_entry`: the message "could not fetch essential information" is created inside a `try` and immediately replaced by the general WebSocket message by `except BaseException`. | Users see an unsuitable error message. | fixed | `eb5da46`. Since `eb5da46` the specific `ConfigEntryNotReady` message is kept. | Shown in a test (`known_bug`).  |
| R26 | After `03b0fc3`, writing in WebSocket mode stores the requested value in `coordinator.data` at once. | If the charger rejects (only a warning in the log), HA shows the rejected value until the device reports the key again. | open |  | Derived from the code, behaviour recorded in a test.  |
| R27 | `write_multiple_values_to_keys` returns `{}` in WebSocket mode; `handle_write_result` skips only `None`. | After every successful vehicle selection a false `ERROR` appears in the log ("could not write multiple value"). | fixed | `9e7d62a`. Since `9e7d62a` `handle_write_result` also skips an empty result in WebSocket mode. | Shown in a test (`known_bug`).  |
| R29 | `98af3e0`: if `cableCurrentLimit` is missing in `cll`, there is no longer a limit to 16 A and `adi` is no longer checked; Core devices without the key were limited to be safe before. | Sliders allow higher values; the charger limits an adapter itself. The assumption "only Flex has the key" is not proven. | open |  | Read from the diff, behaviour recorded in a test.  |
| R30 | According to the maintainer (issue #176) the integration resets the maximum current (Max Ampere) at every restart. | A previously set value is lost; the limit then no longer applies until it is set again. | open |  | Statement of the maintainer, **not** replayed by us and no test for it. Whether it comes from the 16 A limiter (R29) or from taking over values at start is open.  |

## Notes

**Addendum to R2:**this is a **regression** from commit `5328e74` ("housekeeping of tasks"). Before, a `GoeChargerApiV2Service` was always created per charger entry and entered its coordinator into the registry, so `configid` worked for every charger. Since `5328e74` the service is only created for the first charger. In addition, after an entry is reloaded (for example by the automatic restart logic after more than 5 connection errors), with several chargers the **old** coordinator stays in the registry; the service then writes through a separate bridge. Read from the diff and the code, not replayed.

The number R28 was deliberately left out; the numbering follows the order of the findings.

## Open assumptions (not checked)

- Behaviour of the charger after a restart with `frc=1` set.
- Whether the charger accepts the PV data key `ids` over WebSocket exactly as over HTTP.
- Actual minimum version of Home Assistant.
