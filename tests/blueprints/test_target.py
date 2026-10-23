"""Routing regressions: render actual YAML and run the upstream service method."""
import pytest

from harness import BlueprintRun, dispatch


@pytest.mark.parametrize("target,entity", [("entry_a", "car_a"), ("entry_b", "car_b"), ("", "car_a")])
@pytest.mark.parametrize("daylight,trigger,connected", [(True, "tick", "on"),
                                                       (False, "tick", "on"),
                                                       (False, "sunset", "off")])
def test_routes_all_paths(target, entity, daylight, trigger, connected):
    run = BlueprintRun(target=target, daylight=daylight, trigger=trigger, connected=connected,
                       inputs={"car_connected_entity": {"entity_id": f"binary_sensor.{entity}"}})
    calls = run.run()
    assert len(calls) == 1
    payload = calls[0]
    if target:
        assert payload["configid"] == target
    else:
        assert "configid" not in payload
    expected = (-1200, 2000, 0) if daylight else (0, 0, 0)
    assert tuple(payload[key] for key in ("pgrid", "ppv", "pakku")) == expected
    writes = dispatch(payload)
    assert len(writes[target or "entry_a"]) == 1
    assert sum(len(value) for value in writes.values()) == 1


def test_legacy_single_charger():
    payload = BlueprintRun().run()[0]
    assert len(dispatch(payload, available=("entry_b",))["entry_b"]) == 1


@pytest.mark.parametrize("target,selection", [
    ("missing", {"entity_id": "binary_sensor.car_a"}),
    ("entry_b", {"entity_id": "binary_sensor.car_a"}),
    ("entry_a", {"entity_id": ["binary_sensor.car_a", "binary_sensor.car_b"]}),
    ("entry_a", {"entity_id": "binary_sensor.missing"}),
    ("entry_a", {"entity_id": []}),
    ("entry_a", {"device_id": "example_device"}),
    ("entry_a", {"area_id": "example_area"}),
    ("entry_a", {"entity_id": "binary_sensor.car_a", "device_id": "example_device"}),
])
@pytest.mark.parametrize("trigger", ["tick", "sunset"])
def test_invalid_target_never_falls_back(target, selection, trigger):
    run = BlueprintRun(target=target, trigger=trigger, inputs={"car_connected_entity": selection})
    assert run.run() == []
    assert "target go-eCharger" in run.stopped


def test_entry_from_wrong_integration_is_rejected():
    run = BlueprintRun(target="entry_a", entries={"entry_a": "other_integration"})
    assert run.run() == []
    assert run.stopped


def test_entry_disappearing_after_render_does_not_select_another_charger():
    payload = BlueprintRun(target="entry_a").run()[0]
    with pytest.raises(KeyError):
        dispatch(payload, available=("entry_b",))


def test_string_and_list_car_selectors():
    for selection in ("binary_sensor.car_a", ["binary_sensor.car_a"]):
        assert len(BlueprintRun(target="entry_a", inputs={
            "car_connected_entity": {"entity_id": selection}}).run()) == 1


@pytest.mark.parametrize("daylight,connected,second", [(True, "off", 0), (False, "off", 0),
                                                      (False, "on", 5), (False, "on", 25)])
def test_no_extra_calls(daylight, connected, second):
    assert BlueprintRun(daylight=daylight, connected=connected, second=second).run() == []


def test_night_thirty_second_tick():
    assert len(BlueprintRun(daylight=False, second=30).run()) == 1


def invalid_target_run(second):
    return BlueprintRun(target="entry_a", second=second,
                        inputs={"car_connected_entity": {"entity_id": ["binary_sensor.car_b"]}})


def test_invalid_target_is_not_logged_as_error():
    run = invalid_target_run(second=0)
    assert run.run() == [] and run.stopped and run.stop_error is False


@pytest.mark.parametrize("second,expected", [(0, 1), (4, 1), (5, 0), (30, 0), (55, 0)])
def test_invalid_target_notifies_at_most_once_per_minute(second, expected):
    run = invalid_target_run(second)
    run.run()
    assert len(run.notifications) == expected


def test_valid_target_creates_no_notification():
    run = BlueprintRun(target="entry_a", inputs={"car_connected_entity": {"entity_id": ["binary_sensor.car_a"]}})
    assert len(run.run()) == 1 and run.notifications == []
