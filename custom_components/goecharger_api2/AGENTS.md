# AGENTS.md for `custom_components/goecharger_api2/`

Read the [root `AGENTS.md`](../../AGENTS.md) first. This file adds what you need when you change the integration code. The maintainer should look at this file closely: it describes how his code is meant to be changed.

## Two data paths, and what a write returns

The integration reads and writes over a **WebSocket** (when the config entry has a password) or over **HTTP polling** (local or cloud). Both paths are in use, and they return different results for the same write. Change them together and test both.

| Call (bridge) | WebSocket | HTTP |
|---|---|---|
| `write_value_to_key(key, value)` | sends `setValue` and returns `{key: value}` at once; with `require_ack=True` it waits up to 3 seconds for the device's answer and returns `{}` if it does not confirm | `GET /api/set`, returns `{key: value}` or `{"err": ...}` |
| `write_multiple_values_to_keys(...)` | sends the keys one after another and returns `{}` | one request, returns the result dict |

`GoeChargerDataUpdateCoordinator.async_write_key(...)` and `async_write_multiple_keys(...)` wrap these calls, refuse to write during the error pause (2 minutes after a connection error) or a planned restart (`ValueError`), and pass the result to `handle_write_result`. An entity writes through the coordinator, never through the bridge.

## Add a key or an entity

1. **Look the key up in the official table** (name, read/write, type, category). Do not rely on memory or on another integration.
2. **`pygoecharger_ha/keys.py`:** add a `Tag` with `ApiKey(key=..., cat=CAT.CONFIG|STATUS|OTHER|CONSTANT, writeable=...)`. The flags must match the official table (`test_write_flag_matches_documentation`, `test_category_matches_documentation`). If the key was listed as unsupported in `tests/integration/contract/classification.json`, remove that entry.
3. **`pygoecharger_ha/const.py`:** HTTP polling reads only keys that are in a filter. Add a status key to `FILTER_ALL_STATES`, a configuration key to `FILTER_ALL_CONFIG`, and a controller key to the matching `FILTER_CONTROLER_*`. The WebSocket delivers keys without a filter, except those in `API_KEYS_TO_IGNORE_FROM_WS`.
4. **`const.py`:** add an entity description to the list of its platform (`SENSOR_SENSORS`, `NUMBER_SENSORS`, `SELECT_SENSORS`, `SWITCH_SENSORS`, `BINARY_SENSORS`, `BUTTONS`), or to the `CONTROLLER_*` list for a controller. Copy a neighbouring description (for example `LBR` in `NUMBER_SENSORS`). Rarely needed entities are disabled by default (`entity_registry_enabled_default=False`). A current that a 16 A limit must cap has `check_16a_limit=True`.
5. **`translations/en.json`, `de.json`, `fr.json`:** add the name under `entity.<platform>.<key>.name` in all three.
6. **Do not write a platform-specific branch for the new key.** The platforms are generic classes that read the description. A key that needs its own behaviour is a question for the maintainer (see below).
7. **Tests first** (root rules): the contract tests and `test_entity_ids.py` (it will list your new entity as `added`; see `tests/AGENTS.md`) show where the new key must appear.

## Chargers and controllers

A config entry is either a charger or a controller (`intg_type`). They have different keys, filters and entity lists. A controller has no `tcl` and no `cll`. Before you read or write a key, check the key table of that device type (`tests/integration/contract/controller_keys.json` for controllers).

## Things you ask the maintainer about first

- A key that needs behaviour of its own. `Tag.TCL` has extra methods (`tag_func_*`, defined in `keys.py`); the comment next to it in `keys.py` shows that the maintainer is not happy with this mechanism. Do not extend it without asking.
- Data stored in a config entry: a change needs a new `CONFIG_VERSION` or minor version and a step in `async_migrate_entry`. Existing users' entries are migrated with it.
- Entity IDs and `unique_id`s: they are built from the key (and an index for list entries). Never change them.
- A service: `service.py`, `services.yaml`, the `SERVICE_*` constants and the translations belong together. Without `configid` a service call is refused when more than one charger is set up (ADR-0010).

## Pitfalls found in this code

Check these before you change the related code (the risk register has the evidence).

- **Two data paths.** See above ([R027](../../docs/architecture/risks/R027-false-error-after-a-successful-multiple-write.md), [R001](../../docs/architecture/risks/R001-stop-charging-locks-the-charger-after-a-write-error.md), [R004](../../docs/architecture/risks/R004-error-handling-for-multiple-writes-calls-the-wrong-sign.md)).
- **Chargers and controllers differ** ([R029](../../docs/architecture/risks/R029-without-cablecurrentlimit-there-is-no-limit-to-16-a-any.md), #177).
- **Several chargers in one Home Assistant.** State per entry (service registry, counters) is added and removed per entry ([R002](../../docs/architecture/risks/R002-multi-charger-registry-incomplete.md), [R003](../../docs/architecture/risks/R003-active-charger-counter-with-controller-entries.md)).
- **Broad `except`.** `except BaseException` also catches cancellation and replaces a specific message by a general one ([R025](../../docs/architecture/risks/R025-specific-start-error-message-is-covered-up.md)). Catch what you can handle.
- **Values from callers are not trusted.** Check numbers for finiteness (`NaN`, `inf`) before they go to a charger ([R005](../../docs/architecture/risks/R005-pgrid-without-a-finiteness-check.md)).
- **Settings survive a restart.** A value the user set must still be there afterwards ([R030](../../docs/architecture/risks/R030-max-ampere-is-reset-at-every-restart.md), reported by the maintainer, not yet reproduced).
- **Old values after a failed read are intended** ([R020](../../docs/architecture/risks/R020-old-values-stay-after-a-failed-read.md)). Do not "fix" it.

## Code

- Match the surrounding code: naming, comment density, `_LOGGER` levels, f-strings, 4 spaces. There is no formatter. Do not reformat lines you do not change.
- The code is asynchronous. No blocking input or output in the event loop.
- Do not log or store tokens and passwords (not in logs, device info or entity attributes).
- Home Assistant APIs newer than the minimum version in `hacs.json` need a question first ([R011](../../docs/architecture/risks/R011-bcrypt-missing-in-the-manifest-minimum-home-assistant-v.md)).
