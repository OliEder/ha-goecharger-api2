"""Input failures must not become plausible surplus or incomplete power sums."""
from collections import Counter

import pytest

from harness import BlueprintRun


BAD_VALUES = ["unknown", "unavailable", "not a number", "", "NaN", "inf", "-inf", "1e999"]


@pytest.mark.parametrize("bad", BAD_VALUES)
@pytest.mark.parametrize("source", ["sensor.grid", "sensor.pv", "sensor.battery"])
def test_bad_used_source_skips_whole_update(source, bad):
    run = BlueprintRun(inputs={"battery_entities": ["sensor.battery"]},
                       states={"sensor.battery": "0", source: bad})
    assert run.run() == []
    assert run.notifications == []


@pytest.mark.parametrize("input_name,value", [
    ("grid_single_entity", "sensor.missing"), ("pv_entities", ["sensor.missing"]),
    ("battery_entities", ["sensor.missing"]),
])
def test_missing_entity(input_name, value):
    assert BlueprintRun(inputs={input_name: value}).run() == []


@pytest.mark.parametrize("grid", ["0", "1200", "-1200"])
def test_real_zero_import_and_export(grid):
    payload = BlueprintRun(states={"sensor.grid": grid, "sensor.pv": "0"}).run()[0]
    assert payload == {"pgrid": int(grid), "ppv": 0, "pakku": 0}


def dual_inputs():
    return {"grid_single_entity": None, "grid_consumption_entity": "sensor.import",
            "grid_feedin_entity": "sensor.export"}


@pytest.mark.parametrize("missing", ["sensor.import", "sensor.export"])
def test_dual_missing_input_cannot_become_export(missing):
    states = {"sensor.import": "1500", "sensor.export": "1000", missing: "unavailable"}
    assert BlueprintRun(inputs=dual_inputs(), states=states).run() == []


def test_dual_valid():
    payload = BlueprintRun(inputs=dual_inputs(), states={
        "sensor.import": "1500", "sensor.export": "1000"}).run()[0]
    assert payload["pgrid"] == 500


@pytest.mark.parametrize("missing", ["grid_consumption_entity", "grid_feedin_entity"])
def test_incomplete_dual_does_not_fall_back_to_phases(missing):
    inputs = dict(dual_inputs(), grid_phase_entities=["sensor.l1", "sensor.l2", "sensor.l3"])
    inputs[missing] = None
    assert BlueprintRun(inputs=inputs, states={
        "sensor.l1": "-1000", "sensor.l2": "-1000", "sensor.l3": "-1000"}).run() == []


@pytest.mark.parametrize("missing_phase", ["sensor.l1", "sensor.l2", "sensor.l3"])
def test_missing_phase_never_yields_partial_sum(missing_phase):
    states = {"sensor.l1": "-1000", "sensor.l2": "-2000", "sensor.l3": "500",
              missing_phase: "unavailable"}
    run = BlueprintRun(inputs={"grid_single_entity": None,
        "grid_phase_entities": ["sensor.l1", "sensor.l2", "sensor.l3"]}, states=states)
    assert run.run() == []


@pytest.mark.parametrize("phases", [[], ["sensor.l1"], ["sensor.l1", "sensor.l2"],
    ["sensor.l1", "sensor.l2", "sensor.l3", "sensor.l4"], ["sensor.l1"] * 3])
def test_phase_method_requires_three_distinct_entities(phases):
    assert BlueprintRun(inputs={"grid_single_entity": None, "grid_phase_entities": phases},
                        states={f"sensor.l{i}": "0" for i in range(1, 5)}).run() == []


def test_three_phases_and_inversion():
    payload = BlueprintRun(inputs={"grid_single_entity": None,
        "grid_phase_entities": ["sensor.l1", "sensor.l2", "sensor.l3"],
        "grid_phases_invert": True}, states={
        "sensor.l1": "1000", "sensor.l2": "2000", "sensor.l3": "-500"}).run()[0]
    assert payload["pgrid"] == -2500


def test_unused_grid_inputs_do_not_block_selected_single():
    assert len(BlueprintRun(inputs={"grid_consumption_entity": "sensor.missing",
                                   "grid_phase_entities": ["sensor.missing"]}).run()) == 1


def test_failed_single_does_not_fall_back_to_healthy_dual():
    inputs = dict(dual_inputs(), grid_single_entity="sensor.missing")
    assert BlueprintRun(inputs=inputs, states={"sensor.import": "0", "sensor.export": "1000"}).run() == []


@pytest.mark.parametrize("enabled,entities", [(False, ["sensor.missing"]), (True, []), (False, [])])
def test_intentionally_absent_battery(enabled, entities):
    payload = BlueprintRun(inputs={"battery_enabled": enabled, "battery_entities": entities}).run()[0]
    assert payload["pakku"] == 0


@pytest.mark.parametrize("source_list", ["pv_entities", "battery_entities"])
def test_multiple_sources_must_all_be_available(source_list):
    assert BlueprintRun(inputs={source_list: ["sensor.first", "sensor.missing"]},
                        states={"sensor.first": "1200"}).run() == []


def test_empty_pv_is_invalid():
    assert BlueprintRun(inputs={"pv_entities": []}).run() == []


def test_multiple_sources_inversion_and_kw_conversion():
    payload = BlueprintRun(inputs={"power_multiplier": 1000,
        "grid_single_invert": True, "pv_entities": ["sensor.pv1", "sensor.pv2"],
        "pv_invert": True, "battery_entities": ["sensor.b1", "sensor.b2"],
        "battery_invert": True}, states={"sensor.grid": "1.25", "sensor.pv1": "-2",
        "sensor.pv2": "-0.75", "sensor.b1": "0.25", "sensor.b2": "0.5"}).run()[0]
    assert payload == {"pgrid": -1250, "ppv": 2750, "pakku": -750}


def test_rounding_after_conversion():
    payload = BlueprintRun(inputs={"power_multiplier": 1000}, states={
        "sensor.grid": "-0.1234", "sensor.pv": "0.5678"}).run()[0]
    assert payload["pgrid"] == -123
    assert payload["ppv"] == 568


@pytest.mark.parametrize("multiplier", [0, -1, "invalid", "NaN", "inf"])
def test_invalid_multiplier(multiplier):
    assert BlueprintRun(inputs={"power_multiplier": multiplier}).run() == []


@pytest.mark.parametrize("source", ["grid", "pv", "battery"])
def test_overflow_after_unit_conversion(source):
    assert BlueprintRun(inputs={"power_multiplier": 1000, "battery_entities": ["sensor.battery"]},
        states={"sensor.battery": "0", f"sensor.{source}": "1e308"}).run() == []


def test_overflow_of_sum():
    assert BlueprintRun(inputs={"pv_entities": ["sensor.first", "sensor.second"]},
                        states={"sensor.first": "1e308", "sensor.second": "1e308"}).run() == []


@pytest.mark.parametrize("target,entity", [("", "car_a"), ("entry_a", "car_a"), ("entry_b", "car_b")])
@pytest.mark.parametrize("trigger,connected", [("tick", "on"), ("sunset", "off")])
@pytest.mark.parametrize("bad", ["unavailable", "NaN", "inf"])
def test_night_and_sunset_zeros_survive_invalid_measurements(target, entity, trigger, connected, bad):
    run = BlueprintRun(target=target, daylight=False, trigger=trigger, connected=connected,
                       inputs={"car_connected_entity": {"entity_id": f"binary_sensor.{entity}"}},
                       states={"sensor.grid": bad, "sensor.pv": bad})
    payload = run.run()[0]
    assert (payload["pgrid"], payload["ppv"], payload["pakku"]) == (0, 0, 0)
    assert payload.get("configid", "") == target


def test_recovers_on_next_valid_tick():
    assert BlueprintRun(states={"sensor.grid": "unavailable"}).run() == []
    assert BlueprintRun(states={"sensor.grid": "-500"}).run()[0]["pgrid"] == -500


def test_validation_and_arithmetic_use_one_sample_per_source():
    run = BlueprintRun(inputs={"pv_entities": ["sensor.pv", "sensor.pv"]})
    reads = Counter()

    def changing_state(entity):
        reads[entity] += 1
        return run.states.get(entity, "unknown") if reads[entity] == 1 else "unavailable"

    run.env.globals["states"] = changing_state
    payload = run.run()[0]
    assert payload["pgrid"] == -1200
    assert payload["ppv"] == 4000  # Existing sum semantics are unchanged.
    assert reads == {"sensor.grid": 1, "sensor.pv": 1}


@pytest.mark.parametrize("bad", BAD_VALUES)
def test_policy_zero_sends_zeros(bad):
    run = BlueprintRun(inputs={"invalid_data_policy": "zero"}, states={"sensor.grid": bad})
    assert run.run() == [{"pgrid": 0, "ppv": 0, "pakku": 0}]
    assert run.notifications == []


def test_policy_zero_targets_selected_charger():
    run = BlueprintRun(inputs={"invalid_data_policy": "zero", "charger_config_entry": "entry_a",
                               "car_connected_entity": {"entity_id": ["binary_sensor.car_a"]}},
                       states={"sensor.grid": "unavailable"})
    assert run.run() == [{"pgrid": 0, "ppv": 0, "pakku": 0, "configid": "entry_a"}]


@pytest.mark.parametrize("bad", BAD_VALUES)
def test_policy_notify_skips_and_notifies(bad):
    run = BlueprintRun(inputs={"invalid_data_policy": "notify"}, states={"sensor.pv": bad})
    assert run.run() == []
    assert len(run.notifications) == 1
    assert run.notifications[0]["notification_id"].endswith("automation.pv_surplus")


@pytest.mark.parametrize("policy", ["keep", "zero", "notify"])
def test_valid_measurements_ignore_policy(policy):
    run = BlueprintRun(inputs={"invalid_data_policy": policy})
    calls = run.run()
    assert len(calls) == 1 and calls[0] != {"pgrid": 0, "ppv": 0, "pakku": 0}
    assert run.notifications == []


HELPER = "input_datetime.pv_last_valid"
NOW = 1_000_000_000.0


def grace_run(age, policy="zero", grace=60, helper_state=None, **kwargs):
    """Invalid grid with a helper whose last valid sample is `age` seconds old."""
    state = helper_state if helper_state is not None else BlueprintRun.stamp(NOW - age)
    return BlueprintRun(inputs={"invalid_data_policy": policy, "last_valid_helper": HELPER,
                                "invalid_data_grace": grace},
                        states={"sensor.grid": "unavailable", HELPER: state}, now_ts=NOW, **kwargs)


@pytest.mark.parametrize("policy", ["zero", "notify"])
def test_grace_period_defers_reaction(policy):
    run = grace_run(age=30, policy=policy)
    assert run.run() == [] and run.notifications == []


def test_grace_period_boundary_is_exclusive():
    assert grace_run(age=60).run() == []


def test_grace_period_expired_zero():
    assert grace_run(age=61).run() == [{"pgrid": 0, "ppv": 0, "pakku": 0}]


def test_grace_period_expired_notify():
    run = grace_run(age=61, policy="notify")
    assert run.run() == [] and len(run.notifications) == 1


def test_grace_period_keep_never_reacts():
    run = grace_run(age=100000, policy="keep")
    assert run.run() == [] and run.notifications == []


@pytest.mark.parametrize("state", ["unknown", "unavailable", "", "garbage"])
def test_empty_or_unknown_helper_counts_as_expired(state):
    assert grace_run(age=0, helper_state=state).run() == [{"pgrid": 0, "ppv": 0, "pakku": 0}]


def test_no_helper_reacts_immediately():
    run = BlueprintRun(inputs={"invalid_data_policy": "zero"}, states={"sensor.grid": "unavailable"})
    assert run.run() == [{"pgrid": 0, "ppv": 0, "pakku": 0}] and run.helper_writes == []


@pytest.mark.parametrize("age,writes", [(0, 0), (30, 0), (31, 1), (500, 1)])
def test_helper_refresh_is_throttled_to_half_grace(age, writes):
    run = BlueprintRun(inputs={"last_valid_helper": HELPER, "invalid_data_grace": 60},
                       states={HELPER: BlueprintRun.stamp(NOW - age)}, now_ts=NOW)
    assert len(run.run()) == 1
    assert run.helper_writes == ([{"entity_id": HELPER, "timestamp": int(NOW)}] if writes else [])


def test_empty_helper_is_initialised_on_first_valid_sample():
    run = BlueprintRun(inputs={"last_valid_helper": HELPER}, states={HELPER: "unknown"}, now_ts=NOW)
    run.run()
    assert run.helper_writes == [{"entity_id": HELPER, "timestamp": int(NOW)}]


def test_invalid_data_never_refreshes_helper():
    run = grace_run(age=500)
    run.run()
    assert run.helper_writes == []


def test_no_helper_never_writes():
    run = BlueprintRun()
    assert len(run.run()) == 1 and run.helper_writes == []


def test_night_does_not_touch_helper():
    run = BlueprintRun(inputs={"last_valid_helper": HELPER}, states={HELPER: "unknown"},
                       daylight=False, second=0, now_ts=NOW)
    run.run()
    assert run.helper_writes == []


@pytest.mark.parametrize("second,expected", [(0, 1), (4, 1), (5, 0), (30, 0), (55, 0)])
def test_policy_notify_is_throttled_to_once_per_minute(second, expected):
    run = BlueprintRun(inputs={"invalid_data_policy": "notify"}, states={"sensor.grid": "unavailable"},
                       second=second)
    assert run.run() == [] and len(run.notifications) == expected
