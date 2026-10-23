"""Input failures must not become plausible surplus or incomplete power sums."""
from collections import Counter

import os
import time

import pytest

from harness import BlueprintRun


def skip_run(inputs=None, **kwargs):
    """Strict run: a bad battery is invalid and invalid data is skipped silently.

    `[]` therefore means "no update was sent" for every kind of bad source.
    """
    return BlueprintRun(inputs={"invalid_data_policy": "keep",
                                "battery_unavailable_policy": "invalid", **(inputs or {})}, **kwargs)


BAD_VALUES = ["unknown", "unavailable", "not a number", "", "NaN", "inf", "-inf", "1e999"]


@pytest.mark.parametrize("bad", BAD_VALUES)
@pytest.mark.parametrize("source", ["sensor.grid", "sensor.pv", "sensor.battery"])
def test_bad_used_source_skips_whole_update(source, bad):
    run = skip_run(inputs={"battery_entities": ["sensor.battery"]},
                       states={"sensor.battery": "0", source: bad})
    assert run.run() == []
    assert run.notifications == []


@pytest.mark.parametrize("input_name,value", [
    ("grid_single_entity", "sensor.missing"), ("pv_entities", ["sensor.missing"]),
    ("battery_entities", ["sensor.missing"]),
])
def test_missing_entity(input_name, value):
    assert skip_run(inputs={input_name: value}).run() == []


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
    assert skip_run(inputs=dual_inputs(), states=states).run() == []


def test_dual_valid():
    payload = BlueprintRun(inputs=dual_inputs(), states={
        "sensor.import": "1500", "sensor.export": "1000"}).run()[0]
    assert payload["pgrid"] == 500


@pytest.mark.parametrize("missing", ["grid_consumption_entity", "grid_feedin_entity"])
def test_incomplete_dual_does_not_fall_back_to_phases(missing):
    inputs = dict(dual_inputs(), grid_phase_entities=["sensor.l1", "sensor.l2", "sensor.l3"])
    inputs[missing] = None
    assert skip_run(inputs=inputs, states={
        "sensor.l1": "-1000", "sensor.l2": "-1000", "sensor.l3": "-1000"}).run() == []


@pytest.mark.parametrize("missing_phase", ["sensor.l1", "sensor.l2", "sensor.l3"])
def test_missing_phase_never_yields_partial_sum(missing_phase):
    states = {"sensor.l1": "-1000", "sensor.l2": "-2000", "sensor.l3": "500",
              missing_phase: "unavailable"}
    run = skip_run(inputs={"grid_single_entity": None,
        "grid_phase_entities": ["sensor.l1", "sensor.l2", "sensor.l3"]}, states=states)
    assert run.run() == []


@pytest.mark.parametrize("phases", [["sensor.l1"], ["sensor.l1", "sensor.l2"], ["sensor.l1"] * 3])
def test_incomplete_or_duplicate_phases_are_invalid(phases):
    assert skip_run(inputs={"grid_single_entity": None, "grid_phase_entities": phases},
                    states={f"sensor.l{i}": "0" for i in range(1, 5)}).run() == []


def test_no_grid_method_selected_sends_pgrid_zero():
    payload = BlueprintRun(inputs={"grid_single_entity": None}).run()
    assert payload == [{"pgrid": 0, "ppv": 2000, "pakku": 0}]


def test_more_than_three_phases_use_the_first_three():
    payload = BlueprintRun(inputs={
        "grid_single_entity": None,
        "grid_phase_entities": ["sensor.l1", "sensor.l2", "sensor.l3", "sensor.l4"]},
        states={"sensor.l1": "100", "sensor.l2": "200", "sensor.l3": "300", "sensor.l4": "9999"}).run()
    assert payload[0]["pgrid"] == 600


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
    assert skip_run(inputs=inputs, states={"sensor.import": "0", "sensor.export": "1000"}).run() == []


@pytest.mark.parametrize("enabled,entities", [(False, ["sensor.missing"]), (True, []), (False, [])])
def test_intentionally_absent_battery(enabled, entities):
    payload = BlueprintRun(inputs={"battery_enabled": enabled, "battery_entities": entities}).run()[0]
    assert payload["pakku"] == 0


@pytest.mark.parametrize("source_list", ["pv_entities", "battery_entities"])
def test_multiple_sources_must_all_be_available(source_list):
    assert skip_run(inputs={source_list: ["sensor.first", "sensor.missing"]},
                        states={"sensor.first": "1200"}).run() == []


def test_empty_pv_is_invalid():
    assert skip_run(inputs={"pv_entities": []}).run() == []


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
    assert skip_run(inputs={"power_multiplier": multiplier}).run() == []


@pytest.mark.parametrize("source", ["grid", "pv", "battery"])
def test_overflow_after_unit_conversion(source):
    assert skip_run(inputs={"power_multiplier": 1000, "battery_entities": ["sensor.battery"]},
        states={"sensor.battery": "0", f"sensor.{source}": "1e308"}).run() == []


def test_overflow_of_sum():
    assert skip_run(inputs={"pv_entities": ["sensor.first", "sensor.second"]},
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
    assert skip_run(states={"sensor.grid": "unavailable"}).run() == []
    assert skip_run(states={"sensor.grid": "-500"}).run()[0]["pgrid"] == -500


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


def test_default_policy_is_zero():
    """A charger left on stale averages can charge from the grid, so zero is the default."""
    assert BlueprintRun().inputs["invalid_data_policy"] == "zero"


@pytest.mark.parametrize("source", ["sensor.grid", "sensor.pv"])
@pytest.mark.parametrize("bad", BAD_VALUES)
def test_default_sends_zero_for_invalid_measurement(source, bad):
    assert BlueprintRun(states={source: bad}).run() == [{"pgrid": 0, "ppv": 0, "pakku": 0}]


def test_default_still_sends_real_data_when_valid():
    assert BlueprintRun().run() == [{"pgrid": -1200, "ppv": 2000, "pakku": 0}]


@pytest.mark.parametrize("bad", BAD_VALUES)
def test_default_battery_unavailable_sends_battery_zero_and_real_data(bad):
    run = BlueprintRun(inputs={"battery_entities": ["sensor.battery"]},
                       states={"sensor.battery": bad})
    assert run.run() == [{"pgrid": -1200, "ppv": 2000, "pakku": 0}]
    assert run.notifications == []


def test_default_battery_policy_is_zero():
    assert BlueprintRun().inputs["battery_unavailable_policy"] == "zero"


def test_one_bad_battery_entity_does_not_produce_a_partial_sum():
    run = BlueprintRun(inputs={"battery_entities": ["sensor.bat1", "sensor.bat2"]},
                       states={"sensor.bat1": "500", "sensor.bat2": "unavailable"})
    assert run.run()[0]["pakku"] == 0


def test_valid_batteries_are_summed():
    run = BlueprintRun(inputs={"battery_entities": ["sensor.bat1", "sensor.bat2"]},
                       states={"sensor.bat1": "500", "sensor.bat2": "250"})
    assert run.run()[0]["pakku"] == 750


@pytest.mark.parametrize("reaction,expected", [
    ("zero", [{"pgrid": 0, "ppv": 0, "pakku": 0}]), ("keep", []), ("notify", [])])
def test_battery_policy_invalid_uses_the_general_reaction(reaction, expected):
    run = BlueprintRun(inputs={"battery_entities": ["sensor.battery"], "invalid_data_policy": reaction,
                               "battery_unavailable_policy": "invalid"},
                       states={"sensor.battery": "unavailable"})
    assert run.run() == expected


def test_battery_policy_ignored_when_battery_disabled():
    run = BlueprintRun(inputs={"battery_enabled": False, "battery_entities": ["sensor.battery"],
                               "battery_unavailable_policy": "invalid"},
                       states={"sensor.battery": "unavailable"})
    assert run.run() == [{"pgrid": -1200, "ppv": 2000, "pakku": 0}]


def test_other_sources_still_invalid_with_battery_zero_policy():
    run = BlueprintRun(inputs={"battery_entities": ["sensor.battery"]},
                       states={"sensor.battery": "unavailable", "sensor.pv": "unavailable"})
    assert run.run() == [{"pgrid": 0, "ppv": 0, "pakku": 0}]


def test_overflowing_battery_total_falls_under_the_general_reaction():
    run = BlueprintRun(inputs={"power_multiplier": 1000, "battery_entities": ["sensor.battery"]},
                       states={"sensor.battery": "1e308"})
    assert run.run() == [{"pgrid": 0, "ppv": 0, "pakku": 0}]


@pytest.fixture
def process_time_zone():
    """Run with another process time zone than the simulated HA one (Europe/Berlin)."""
    def use(zone):
        os.environ["TZ"] = zone
        time.tzset()
    saved = os.environ.get("TZ")
    yield use
    if saved is None:
        os.environ.pop("TZ", None)
    else:
        os.environ["TZ"] = saved
    time.tzset()


@pytest.mark.parametrize("zone", ["UTC", "America/New_York", "Asia/Tokyo", "Europe/Berlin"])
@pytest.mark.parametrize("age,expired", [(10, False), (59, False), (61, True)])
def test_grace_period_does_not_depend_on_the_process_time_zone(process_time_zone, zone, age, expired):
    process_time_zone(zone)
    run = grace_run(age=age)
    assert run.run() == ([{"pgrid": 0, "ppv": 0, "pakku": 0}] if expired else [])


@pytest.mark.parametrize("zone", ["UTC", "America/New_York", "Asia/Tokyo"])
@pytest.mark.parametrize("age,writes", [(10, 0), (31, 1)])
def test_helper_refresh_does_not_depend_on_the_process_time_zone(process_time_zone, zone, age, writes):
    process_time_zone(zone)
    run = BlueprintRun(inputs={"last_valid_helper": HELPER, "invalid_data_grace": 60},
                       states={HELPER: BlueprintRun.stamp(NOW - age)}, now_ts=NOW)
    run.run()
    assert len(run.helper_writes) == writes


def test_helper_in_the_future_counts_as_expired():
    assert grace_run(age=-3600).run() == [{"pgrid": 0, "ppv": 0, "pakku": 0}]


def test_helper_in_the_future_is_rewritten():
    run = BlueprintRun(inputs={"last_valid_helper": HELPER}, states={HELPER: BlueprintRun.stamp(NOW + 3600)},
                       now_ts=NOW)
    run.run()
    assert len(run.helper_writes) == 1


@pytest.mark.parametrize("policy", ["Zero", "ZERO", "something_else", ""])
def test_unknown_policy_value_falls_back_to_zero(policy):
    run = BlueprintRun(inputs={"invalid_data_policy": policy}, states={"sensor.grid": "unavailable"})
    assert run.run() == [{"pgrid": 0, "ppv": 0, "pakku": 0}]


@pytest.mark.parametrize("second,expected", [(0, 1), (4, 1), (5, 0), (30, 0)])
def test_notify_notification_is_dismissed_once_data_is_valid(second, expected):
    run = BlueprintRun(inputs={"invalid_data_policy": "notify"}, second=second)
    run.run()
    assert len(run.dismissed) == expected
    assert all(i.endswith("automation.pv_surplus") for i in run.dismissed)


@pytest.mark.parametrize("policy", ["zero", "keep"])
def test_no_dismiss_call_for_other_policies(policy):
    run = BlueprintRun(inputs={"invalid_data_policy": policy}, second=0)
    run.run()
    assert run.dismissed == []


def test_notification_stays_while_data_is_invalid():
    run = BlueprintRun(inputs={"invalid_data_policy": "notify"}, states={"sensor.grid": "unavailable"})
    run.run()
    assert run.dismissed == [] and len(run.notifications) == 1
