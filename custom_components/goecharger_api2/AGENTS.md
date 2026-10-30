# AGENTS.md for `custom_components/goecharger_api2/`

Read the [root `AGENTS.md`](../../AGENTS.md) first. This file adds what you need when you change the integration code.

## Two data paths, and what a write returns

The integration reads and writes over a **WebSocket** (when the config entry has a password) or over **HTTP polling** (local or cloud). Both paths are in use, and they return different results for the same write. Change them together and test both.

| Call (bridge) | WebSocket | HTTP |
|---|---|---|
| `write_value_to_key(key, value)` | sends `setValue` and returns `{key: value}` at once; with `require_ack=True` it waits up to 3 seconds for the device's answer and returns `{}` if it does not confirm | `GET /api/set`, returns `{key: value}` or `{"err": ...}` |
| `write_multiple_values_to_keys(...)` | sends the keys one after another and returns `{}` | one request, returns the result dict |
| a failed write | `{}` if the send fails | `{}` on a status other than 200 or on an exception |

A button press is answered with `{key: value}` on the WebSocket (it has no effect there). `GoeChargerDataUpdateCoordinator.async_write_key(...)` and `async_write_multiple_keys(...)` wrap these calls, refuse to write during the error pause (2 minutes after a connection error) or a planned restart (`ValueError`), and pass the result to `handle_write_result`. An entity writes through the coordinator, never through the bridge.

## Add a key or an entity

1. **Look the key up in the official table** (name, read/write, type, category). Do not rely on memory or on another integration.
2. **`pygoecharger_ha/keys.py`:** add a `Tag` with `ApiKey(key=..., cat=CAT.CONFIG|STATUS|OTHER|CONSTANT, writeable=...)`. The flags must match the official table (`test_write_flag_matches_documentation`, `test_category_matches_documentation`). If the key was listed as unsupported in `tests/integration/contract/classification.json`, remove that entry.
3. **`pygoecharger_ha/const.py`:** **both paths read only keys that are in a filter.** HTTP asks the device for the filter, and the WebSocket path takes the filtered keys out of the messages it received. Add a status key to `FILTER_ALL_STATES`, a configuration key to `FILTER_ALL_CONFIG`, and a controller key to the matching `FILTER_CONTROLER_*`. (`API_KEYS_TO_IGNORE_FROM_WS` drops keys from the WebSocket delta messages only.) No test checks the filters; check them by hand.
4. **`const.py`:** add an entity description to the list of its platform (`SENSOR_SENSORS`, `NUMBER_SENSORS`, `SELECT_SENSORS`, `SWITCH_SENSORS`, `BINARY_SENSORS`, `BUTTONS`), or to the `CONTROLLER_*` list for a controller. Copy a neighbouring description (for example `LBR` in `NUMBER_SENSORS`). Rarely needed entities are disabled by default (`entity_registry_enabled_default=False`). A current that a 16 A limit must cap has `check_16a_limit=True` (number entities only): it also makes the integration write a lower value to the charger about 15 seconds after setup (`check_and_write_to_16a`, which reads over HTTP). Some keys are excluded on Core wallboxes in `is_valid_charger_entity`. The lists `STRING_INPUT` and `OTHER` in `const.py` are not used; a description there creates no entity.
5. **`translations/`:** add the name under `entity.<platform>.<translation key>.name` in `en.json` and `de.json`, and in `fr.json` where you can (it already lacks entries). The translation key is the lower-case key for a plain entity, `<key>_<idx>` for an entry of a list, `<key>_value` for a lookup and `<key>_delta` for a differential value; an entity with `tuple_idx` needs its `translation_key`. No test checks translations; a missing one only shows up in the log at run time.
6. **Do not write a platform-specific branch for the new key.** The platforms are generic classes that read the description. A key that needs its own behaviour is a question for the maintainer (see below).
7. **Tests first** (root rules). The contract tests check the `Tag` flags and the key lists (a key the official table does not list must be explained in `classification.json` under `undocumented_in_code`; a key newer than the stored table needs `generate_api_keys.py`, see `tests/AGENTS.md`). `test_entity_ids.py` lists your new entity as `added` (see `tests/AGENTS.md`).

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
- **Broad `except`.** `except BaseException` also catches cancellation and replaces a specific message by a general one; the message problem is fixed, but `async_setup_entry` still has the pattern ([R025](../../docs/architecture/risks/R025-specific-start-error-message-is-covered-up.md)). Catch what you can handle.
- **Values from callers are not trusted.** Check numbers for finiteness (`NaN`, `inf`) before they go to a charger ([R005](../../docs/architecture/risks/R005-pgrid-without-a-finiteness-check.md)).
- **Settings survive a restart.** A value the user set must still be there afterwards ([R030](../../docs/architecture/risks/R030-max-ampere-is-reset-at-every-restart.md): the 16 A limiter reset it; fixed for the reporter in `4c7207c`).
- **The 16 A limiter reads over HTTP also in WebSocket mode** ([R033](../../docs/architecture/risks/R033-16-a-limiter-reads-over-http-also-in-websocket-mode.md)). Every other read in WebSocket mode uses `_read_filtered_data_from_ws_source`. A red test for it is on the fork branch `tests/known-bugs-r031-r033`.
- **An unlock write that is not confirmed is reported as success** in `stop_charging` ([R031](../../docs/architecture/risks/R031-stop-charging-does-not-check-the-unlock-and-may-report.md)). Check the answer of every write that undoes a lock.
- **Old values after a failed read are intended** ([R020](../../docs/architecture/risks/R020-old-values-stay-after-a-failed-read.md)). Do not "fix" it.

## Code

The project has no linter, so these rules are the review. Each one says why. They apply to the code **you write or change**; do not rewrite old code to follow them in a change that is about something else (the counts below are from `main` at `e6ee0c3` and show how much old code there is).

- Match the surrounding code: naming, comment density, `_LOGGER` levels, f-strings, 4 spaces. There is no formatter. Do not reformat lines you do not change.
- **Search before you write.** Before a helper, a constant, an entity pattern or a parser, search the integration for the operation (`pygoecharger_ha/`, the lists in `const.py`, the base entity in `__init__.py`). Two implementations of the same thing are a defect even when both work, and the maintainer asked to reuse the existing structure ([#177](https://github.com/marq24/ha-goecharger-api2/pull/177)). If a capability is missing, extend the existing code instead of copying its logic.
- **Behaviour belongs in the descriptions, not in branches.** Do not branch in the code on a key name, a firmware version or a device type when the entity description, a `Tag` flag or a filter can carry it. This is the rule behind "no `if new_tag: ... else`" and behind the data tables of this integration.
- **Check what you call; do not guess.** Read the signature and the return value of the bridge or coordinator method, and of the Home Assistant API, before you use it. The tests install Home Assistant (`requirements_dev.txt`), so its source is on disk: read it. R001 and R027 are callers that handled a return value of the wrong shape.
- **Imports at the top of the module, never inside a function.** There are none inside functions today.
- **Log with `_LOGGER`, never `print`.** There is no `print` today.
- **Catch what you can handle.** Do not add `except BaseException` (it also catches cancellation, [R021](../../docs/architecture/risks/R021-migration-from-2-0-to-2-1-deletes-all-devices.md), [R025](../../docs/architecture/risks/R025-specific-start-error-message-is-covered-up.md)). A new broad `except Exception` must log the type and the message and must not hide a failure from the caller. There are 21 broad handlers today.
- **Do not reach into the private members of another class** (`bridge._read_filtered_data`, `bridge._ws_states`). Add a public method to the class that owns the data ([R010](../../docs/architecture/risks/R010-check-and-write-to-16a-accesses-private-members.md), [R033](../../docs/architecture/risks/R033-16-a-limiter-reads-over-http-also-in-websocket-mode.md)). There are 16 such accesses outside the bridge today.
- **Name timing values.** A wait or a delay (the 300 s of `stop_charging`, the 15 s before the limiter, the 2.5 s refresh, the 3 s acknowledgement) is a named constant, not a number in the call. A reader and a test can then refer to the meaning. There are six number literals in `sleep(...)` today.
- **Annotate new functions** with parameter and return types. About one third of the existing functions have them; do not annotate old code in an unrelated change.
- **Do not add a new module or file for one feature**, and do not copy a block of an existing entity class to change one line: derive or parameterise.
- The code is asynchronous. No blocking input or output in the event loop.
- Do not log or store tokens and passwords (not in logs, device info or entity attributes).
- Home Assistant APIs newer than the minimum version in `hacs.json` need a question first ([R011](../../docs/architecture/risks/R011-bcrypt-missing-in-the-manifest-minimum-home-assistant-v.md)).
