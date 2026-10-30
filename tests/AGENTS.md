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
| `api_keys.json`, `controller_keys.json` | Key names and flags from the **official** tables, written by `generate_api_keys.py` | **No.** Regenerate: `python tests/integration/contract/generate_api_keys.py <path to apikeys-en.md of a checkout of the official repository> <its commit sha> <date> [controller]`. |
| `classification.json` | Documented keys the integration does not support, with group and decision; also explains keys the code uses that the table does not list (group `undocumented_in_code`) | Yes, when a key becomes supported (remove its entry) or when you add an unsupported key knowingly. Stale entries fail a test. |
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
- **Name what a consumer sees if the test fails.** If you cannot, do not add the test. A new test defends one externally observable contract: behaviour, output, a state change, an error that reaches the user, or a parsing boundary.
- **Do not assert wording or constants.** Assert the exception type and a stable part (a key, a translation key, a value the behaviour depends on). An exact message or the value of a constant is a contract only when someone reads or parses it, and the docstring then says who ([R032](../docs/architecture/risks/R032-tests-assert-the-exact-wording-of-messages.md); the maintainer sent new expected texts in #172, so for some messages he is that reader). "A failing call is retried five times" is a test; "the limit is 5" is not.
- **Do not test the text of a source file.** Such a test breaks on a harmless rename and passes while the behaviour is broken. Run the code and assert what it does. The only existing uses of `inspect.getsource` (`test_services_and_setup.py`, `test_versions_16a.py`) are skip conditions that decide whether a rule exists in the release under test; do not copy them.
- **No echo of the input.** Do not assert that a builder copied a fixture into a field, or that a function returns what was already valid input. Assert a transformation, a rejection or a downstream effect.
- **Each row of a parametrised test covers a different branch.** Remove rows that run the same path.
- **One level per behaviour.** When an integration test already proves it, do not add a mock-based test that says the same.
- **A test that waits or retries asserts a bounded result** (the number of attempts, the error that surfaces, the state afterwards), not only that nothing was raised.
- **Leave no state behind.** A test must pass in the full run, not only alone. Whatever it changes at module level (for example `service_module._COORDINATOR_PER_CONFIG_ENTRY_ID_MAP`) is reset by a fixture, as `clean_registry` does, and a patch lives only inside its test.
- **Generated files.** A test may read `api_keys.json` or `controller_keys.json` as input (the contract tests do) but asserts the rule the data encodes, for example the flags of a `Tag` against the official table. The entity ID snapshot is the one deliberate exception; read its diff before you accept a change (see above).

(Adapted from the testing rules of [oh-my-pi](https://github.com/can1357/oh-my-pi/blob/main/AGENTS.md) and from `writing-good-tests`, summarised below.)

## Tools (`tools/`)

`measure.sh` and `build_report.py` produce the test report, `build_testcases.py` the test case list, `build_site.py` the web pages, `build_risk_register.py` the risk documents. They do not run as tests. Do not change them in a change that is about something else.

## Writing good tests (summary of `writing-good-tests`)

If your agent already works with [Superpowers](https://github.com/obra/superpowers), its `test-driven-development` skill points to this guide and you can skip the summary. For everyone else, it follows the guide closely (MIT licence, by Jesse Vincent). **If you can read URLs, read the full guide before you write or change a test. If you cannot, this summary is enough.**

Two rules govern everything: **every test names the break it catches, and every test exercises the real thing.**

1. **Name the break.** Before you write the test body, name the production change that should make the test fail, and say whether that change is a bug or a decision. If you cannot name one, redesign the test around an observable behaviour.
2. **Derive the expected value independently.** Use literals or hand-checked fixtures; tests with a table of literal expected values are preferred. An expectation that the code under test (or its helpers) computes passes whatever the code does. In this repository the official key tables are such an independent source.
3. **No change detectors.** A test that only an intentional decision can fail (the value of a constant, the exact wording of a message, a private structure) fires on every redesign and sleeps through bugs. Test the behaviour that depends on the decision: not "the limit is 5", but "a failing call is retried 5 times and the sixth attempt never happens".
4. **Behaviour, not text.** Do not assert that a file contains a line. Run it with controlled input and assert the output, the side effects or the exit code. Prose for humans needs no test.
5. **Your code, not the framework.** Test the contract your code makes at its boundaries (what it registers, what it sends, what it returns), not how Home Assistant works. If upstream behaviour surprised you, write one narrow characterisation test that names the assumption. Constructors, getters, constants and trivial forwarding get a test only when they validate, normalise, default, derive, enforce or cause a side effect.
6. **Exercise the real thing.**
   - A mock earns no assertions. Never assert on the mock itself; if the mock is what you check, unmock it or delete the assertion.
   - Mock at the right level: learn every side effect of the real method, mock the slow or external level below it, and keep real what the test depends on.
   - Make doubles specific: when arguments, call counts or order are part of the contract, assert them, and give each branch (success, error, malformed answer) its own fixture, so the wrong branch cannot satisfy the test.
   - Mirror real data completely, with all documented fields, not only those your test reads.
   - Production classes carry production methods only; cleanup that only tests need lives in test utilities.
   - When mock set-up outgrows the test, use real components in an integration test (the pattern of this repository).
7. **Ship the tests the behaviour needs, and only those.** Trivial code and prose earn none; a test written to satisfy a process costs maintenance for good.
8. **Mutation check before you finish.** Change the production code in your head: a wrong constant or argument, a wrong branch, a missing state change or side effect, an empty or default return, a missing check for zero, empty, none, unauthorised or malformed input. At least one test should fail for each realistic change. If none does, the behaviour is unprotected or a test is tautological.

**Warning signs:** set-up and assertion share the same object; the test can only fail by a crash; it fails on every intended change and never on accidental breakage; expected values hide behind loops, builders or helpers; the test greps source text; it would still matter if only the framework remained; it exists for coverage and checks no outcome; an assertion fails when you remove the mock; a method is called only from tests; mock set-up is more than half of the test; mocking "just to be safe".

Source: <https://github.com/obra/superpowers/blob/main/skills/test-driven-development/writing-good-tests.md>
