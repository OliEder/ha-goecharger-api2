# AGENTS.md for `tests/`

Read the [root `AGENTS.md`](../AGENTS.md) first. This file adds what you need when you write or change tests here.

## Run

```bash
python -m pytest tests/integration -m "not known_bug and not needs_decision"   # blocking set, must be green
python -m pytest tests/integration -m "known_bug or needs_decision"            # open findings, red on purpose
python -m pytest tests/integration/test_service.py -q                          # one file while you work
```

The whole blocking set runs in seconds. Find the file for your area in the table of `tests/integration/README.md`. Add a test to the file of its area; create a new file only for a new area.

## What the tests use

- **Real code, fake edges.** Bridge and coordinator are the real code. Only the HTTP layer (`aioclient_mock`) and the WebSocket connection (fake socket and session objects, see `test_ws_login_failures.py` and `test_ws_protocol.py`) are fakes. Do not mock the bridge or the coordinator.
- **Builders** in `factories.py`: `make_entry(hass, ...)`, `make_coordinator(hass, ..., websocket=...)` and `make_bridge(hass, ..., websocket=...)`. Use them; do not build config entries by hand.
- **Waiting.** Patch `asyncio.sleep` where the code waits (existing tests show how). A test must not take real seconds.
- **No network.** The framework blocks real sockets. Use invented data (serial `123456`, address `192.0.2.10`), never a real serial number, token or address.

## Contract data (`integration/contract/`)

| File | What it is | May you edit it? |
|---|---|---|
| `api_keys.json`, `controller_keys.json` | Key names and flags from the **official** tables, written by `generate_api_keys.py` | **No.** Regenerate with the script and the commit of the official repository. |
| `classification.json` | Documented keys the integration does not support, with group and decision; also explains keys the code uses that the table does not list | Yes, when a key becomes supported (remove its entry) or when you add an unsupported key knowingly. Stale entries fail a test. |
| `deviations.json` | Known differences between the table and the code (read/write flag, category); their tests are `needs_decision` | Only with a decision of the maintainer. A **new** difference has no marker and blocks at once. |

## Entity IDs

`snapshots/entity_ids.json` holds the expected entity IDs. Adding an entity makes `test_entity_ids_match_snapshot` fail with an `added` list. That is expected: regenerate with

```bash
UPDATE_SNAPSHOT=1 python -m pytest tests/integration/test_entity_ids.py
```

and **read the diff of the snapshot. It may only add IDs.** If it removes or renames an ID, stop: existing users would lose or rewrite entities.

## Writing a test here

- One behaviour per test, with a name that says what should happen. Arrange, act, assert, in this order.
- **The first line of the docstring is the line of this test in the published test case list** (`tests/tools/build_testcases.py`). Make it a plain sentence. The first line of the module docstring describes the file.
- A test follows an outside source: the official tables, the Modbus profile, an observed device answer or a decision of the maintainer. Say which in the docstring where it is not obvious.
- Test both data paths (WebSocket and HTTP) when you change reading or writing; `test_versions_transport_parity.py` is an example.
- A known defect gets the marker `known_bug`, an open decision `needs_decision`, both with a one-line reason. Never use a marker or `skip` to hide a failure of your own change.

## Tools (`tools/`)

`measure.sh` and `build_report.py` produce the test report, `build_testcases.py` the test case list, `build_site.py` the web pages, `build_risk_register.py` the risk documents. They do not run as tests. Do not change them in a change that is about something else.
