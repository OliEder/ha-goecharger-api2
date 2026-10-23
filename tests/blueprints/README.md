# Blueprint regression tests

From the repository root, in an isolated Python 3.12 environment:

```sh
python -m pip install -r tests/blueprints/requirements.txt
python -m pytest tests/blueprints -q
```

Tests load the actual blueprint YAML, resolve input defaults, render its Jinja
templates and evaluate the supported action/condition tree using synthetic
states and entity/config-entry registries. Routing tests additionally execute
the unchanged upstream `set_pv_data` method extracted from `service.py`, with
two fake LAN coordinators. No hardware, credentials or network is used.

This is not a Home Assistant runtime/schema validation or hardware test.
The state/registry helpers and action evaluator are test doubles; HA import,
selector UI and automation traces must still be checked in a disposable HA
instance before release. WAN filtering and firmware behaviour are outside
these tests. No claim is made that stopping transmission stops charging.

## What the tests simulate

- `state_attr(helper, 'timestamp')` is time zone aware and uses a fixed Home
  Assistant time zone (Europe/Berlin). The time zone tests run the test
  process in other zones (UTC, New York, Tokyo) and expect identical results.
  They fail if the blueprint parses the helper state string with
  `as_timestamp` instead, which uses the time zone of the process.
- `persistent_notification.create` / `.dismiss` and
  `input_datetime.set_datetime` are recorded, not executed.
- The harness evaluates `if`, `choose`, `stop` and `condition` steps itself.
  A failing `condition` step ends the whole simulated run, while Home Assistant
  only ends the nested sequence. Keep new actions that follow such a step in
  mind when you extend the tests.
- Each `BlueprintRun` is one tick. Behaviour over several ticks is tested by
  running several instances with the states of each tick.

## Adding a test

Create a `BlueprintRun` with `inputs`, `states`, `second` (for the 5 second
throttling), `now_ts` and `daylight`, call `run()` and assert on the returned
service payloads. Use `notifications`, `dismissed`, `helper_writes` and
`stopped` for the other effects. `skip_run` in `test_measurements.py` selects
the strict policies, so that `[]` means that no update was sent.
