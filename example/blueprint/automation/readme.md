# go-eCharger PV Surplus Charging Blueprint

This blueprint enables automatic PV surplus charging for go-eCharger wallboxes by transmitting solar system data (grid power, PV generation, battery status) to the charger every 5 seconds during the day. At night it sends zero values, so the charger never works with stale surplus data.

## Requirements

- Home Assistant 2024.6.0 or newer
- [go-eCharger API2 integration](https://github.com/marq24/ha-goecharger-api2) installed
- go-eCharger configured for PV surplus charging (ECO mode)
- The "car connected" entity (`binary_sensor`) of the go-eCharger API2 integration

## Features

- **Multiple grid measurement methods**: Single entity, consumption + feed-in, or 3-phase entities
- **Flexible PV setup**: Supports multiple PV entities with automatic summation
- **Battery support**: Optional battery data transmission with configurable inversion
- **Unit conversion**: Configurable multiplier for entities that report kW instead of W
- **Day and night aware**: Real values from sunrise to sunset, zero values at night (see [Data transmission](#data-transmission))
- **Only active with a connected car**: Nothing is sent while no car is plugged in (except one zero push at sunset)
- **Selectable target charger**: Optional, for installations with more than one go-eCharger
- **Safe handling of missing measurements**: A missing or invalid sensor never becomes a made-up value; the reaction is configurable (see [Invalid measurements](#invalid-measurements))
- **Optional grace period**: Tolerates short sensor dropouts before the reaction starts
- **User-friendly UI**: Organized input sections for easy configuration

## Installation

### Option 1: Direct Import
1. Go to **Settings** → **Automations & Scenes** → **Blueprints**
2. Click **Import Blueprint**
3. Use this URL: `https://raw.githubusercontent.com/marq24/ha-goecharger-api2/refs/heads/main/example/blueprint/automation/go-echarger-pv-surplus-data.yaml`

### Option 2: Manual Installation
1. Download `go-echarger-pv-surplus-data.yaml`
2. Place in `/config/blueprints/automation/`
3. Restart Home Assistant
4. Create automation from blueprint

## Configuration

### Target go-eCharger
Select the go-eCharger integration entry when more than one charger is configured.
All three transmission paths (daylight, night and sunset) use this entry.
Create one automation per charger and select its own **Car connected** entity.

Leaving this input empty preserves the service's existing default selection;
the blueprint omits `configid` rather than passing an empty ID. The service
uses its first registered charger, so select an explicit target for multiple chargers.

With an explicit target, select individual Car connected entities belonging to
that same integration entry. Mixed chargers, device/area targets and a removed
or invalid entry stop the run without sending data. This is shown in a persistent
notification (at most once per minute, closed again once the target is valid)
and in the automation trace. It is deliberately not logged as an error,
because it would repeat every 5 seconds.
The blueprint does not silently fall back to another charger.

### Car Connected
Select the "car connected" entity (`binary_sensor`) of your go-eCharger from the API2 integration.
- Example: `binary_sensor.goe_123456_car_0`

### Power Unit Multiplier
The go-eCharger expects **watts**. This factor is applied to grid, PV and battery values before they are sent.
- Entities report **W**: keep the default `1`
- Entities report **kW** (e.g. FoxESS Modbus): set `1000`

The default of `1` keeps the behavior of earlier versions, so existing automations keep working unchanged.

### Grid Power Setup
Choose **ONE** method:

**Single Entity**: Use if you have one entity with positive (import) and negative (export) values
- Example: `sensor.meter_power_now`

**Consumption + Feed-in**: Use separate entities for consumption and feed-in
- Example: `sensor.grid_consumption` + `sensor.grid_feedin`

**3-Phase Entities**: Use individual phase entities (L1, L2, L3)
- Example: `sensor.grid_l1_power`, `sensor.grid_l2_power`, `sensor.grid_l3_power`

### PV Power
- Select all PV entities (multiple supported)
- Entities are automatically summed
- Enable inversion if your PV entities use negative values

### Battery Power
- Optional battery data transmission
- Multiple entities supported with automatic summation
- Convention: Positive = discharging, Negative = charging

## Data Transmission

| Situation | What is sent |
|---|---|
| Sunrise to sunset, car connected | Real values every 5 seconds |
| Night, car connected | Zero values every 30 seconds |
| At sunset | One immediate zero push, regardless of car connection |

### Invalid measurements

Daylight updates require finite numeric states for every used grid and PV
entity and, when enabled, every selected battery entity. `unknown`,
`unavailable`, missing entities, text, NaN and infinity skip the entire update;
they are not replaced with zero or omitted from a partial sum. A real zero is
valid. Each used state is captured once for validation and calculation.
Non-finite totals or unit conversion results also skip the update.

The existing grid method precedence remains single entity, then consumption /
feed-in, then phases. Both consumption and feed-in must be selected; phases need
at least three entities, of which the first three are used and must be distinct.
An incomplete selected method does not fall back to another method. If no grid
method is selected at all, `pgrid` is sent as 0, as in earlier versions. Unused
grid inputs are ignored.

The phase method needs three phase entities. With fewer phases (for example a
two-phase connection), use a sensor for the total grid power with the *Single
Entity* method instead. Earlier versions silently sent `pgrid=0` for fewer than
three phases; now the selection is treated as an invalid measurement.

An empty battery selection means no battery measurement and still sends zero.
Disabling battery transmission ignores any selected battery entities and also
sends zero. An enabled, selected but unavailable battery is handled as
described under *Battery sensor unavailable* below.
At least one PV entity is required. The multiplier must be finite and positive.

The skipped update is visible in the automation trace. Transmission resumes
on the next daylight tick with valid measurements and a connected car. Night
and sunset zeros remain independent of measurement validity.

**Why zero is the default.** The go-eCharger calculates its `pvopt_*` averages
from the last values it has received, no matter how old they are. If the
blueprint merely stopped sending while a measurement is missing, the charger
would go on with the surplus it saw last and could charge from the grid.
Therefore invalid measurements lead to zero values by default, the same values
the blueprint already sends at night. The blueprint does not check source
timestamps or freshness: an old but numeric state passes validation.

#### Reaction to invalid daylight measurements

The input **Reaction to invalid daylight measurements** decides what happens
while a measurement is invalid. In all cases the real, incomplete data is never
sent:

| Option | Behaviour |
|--------|-----------|
| Send zero values (default) | Send `pgrid=0`, `ppv=0`, `pakku=0` (with the selected `configid`). The charger stops relying on stale surplus and drops to its minimum or stops, depending on its PV settings. |
| Skip update and notify | Skip the update and create a persistent notification, about once a minute. The notification is closed again once measurements are valid. The charger keeps its last values and may charge from the grid meanwhile. |
| Keep last values | Skip the update silently. Same risk as above, without a message. Choose this only if continued charging on old values is wanted. |

Valid measurements resume normal transmission on the next daylight tick.
Night and sunset zero values are independent of this setting.

**Example.** Entities report kW (multiplier `1000`): grid consumption 0.2 kW,
feed-in 1.0 kW, PV 3.0 kW, battery -0.5 kW (charging). The values are what the
blueprint sends as `pgrid / ppv / pakku` in watts:

| Situation | Send zero values (default) | Skip update and notify | Keep last values |
|---|---|---|---|
| All measurements valid | -800 / 3000 / -500 | -800 / 3000 / -500 | -800 / 3000 / -500 |
| Feed-in sensor `unavailable` | 0 / 0 / 0 | nothing sent, notification | nothing sent |
| PV sensor `unavailable` | 0 / 0 / 0 | nothing sent, notification | nothing sent |

"Nothing sent" means the charger keeps working with the last values it
received.

#### Battery sensor unavailable

A missing battery reading should not stop PV surplus charging. By default
(**Battery sensor unavailable = Send battery 0**) the blueprint sends
`pakku=0` and keeps all other values real. If any selected battery entity is
unusable, the whole battery value is 0; the remaining entities are not summed,
because a partial sum would be wrong.

With `pakku=0` the charger assumes the battery is neither charging nor
discharging. If your battery charges or discharges with high power, the surplus
the charger sees can be too high or too low until the sensor returns. In that
case choose **Treat as invalid measurement**: the outage is then handled like
any other invalid measurement, with the reaction chosen above (zero values by
default). The setting has no effect when battery transmission is disabled.

Same example, battery sensor `unavailable`:

| Battery sensor unavailable | Reaction to invalid measurements | Sent as `pgrid / ppv / pakku` |
|---|---|---|
| Send battery 0 (default) | any | -800 / 3000 / 0 |
| Treat as invalid measurement | Send zero values | 0 / 0 / 0 |
| Treat as invalid measurement | Skip update and notify | nothing sent, notification |
| Treat as invalid measurement | Keep last values | nothing sent |

#### Optional grace period

Without further setup, the reaction starts with the first invalid tick. A
single `unavailable` sample, for example while an integration reloads, then
already triggers it. To tolerate short dropouts, add a grace period.

**This is optional. The blueprint works without it.**

1. Create a helper: *Settings > Devices & services > Helpers > Create helper >
   Date and/or time*. Enable **both** *Date* and *Time*. Name it, for example,
   `PV blueprint last valid data`.
2. Select it as **Grace period helper** in the automation. Use one helper per
   automation.
3. Set the **Grace period (seconds)**; default 60, minimum 30.
4. **Recommended:** exclude the helper from the recorder, see below.

How it works:

- While all measurements are valid, the blueprint stores the current time in
  the helper. To keep database writes low this happens only when the stored
  time is older than half the grace period (about every 30 seconds at the
  default), not every 5 seconds.
- While measurements are invalid, nothing is sent until the stored time is
  older than the grace period. Because the helper is only refreshed every half
  grace period, the stored time can already be up to half a grace period old
  when the data turns invalid. The reaction therefore starts after **between
  half and the full grace period** without valid data (15 to 30 seconds at the
  minimum of 30, 30 to 60 seconds at the default). After that, the selected
  reaction runs on every 5 second tick until valid data returns.
- During the grace period nothing is sent, so the charger works with its last
  values. Keep it short: a long grace period delays the protection against
  charging on stale values by the same time.
- With *Keep last values* the grace period has no visible effect, because
  nothing is sent in either case.
- An empty or unknown helper counts as expired. After creating the helper, the
  first valid sample initialises it.
- The helper is only written during daylight with a connected car, so it can
  be old after a night or when the car was disconnected. The first invalid
  sample right after such a gap therefore reacts immediately, because the
  grace period is already over.

**Exclude the helper from the recorder.** It is only needed as a current value.
With the default of 60 seconds it is written about every 30 seconds during
daylight, roughly 1,400 times on a sunny day, and every write becomes useless
history in the database. Add this to `configuration.yaml`, with the entity ID
of your helper, and restart Home Assistant:

```yaml
recorder:
  exclude:
    entities:
      - input_datetime.pv_blueprint_last_valid_data
```

The helper must be of type *Date and time*. Its `timestamp` attribute is used
for the age, because it follows the time zone configured in Home Assistant. A
date-only or time-only helper gives a wrong age and is rewritten on every tick.

Example with the default grace period of 60 seconds, per tick (every 5 seconds):

| Age of the time stored in the helper | Measurements valid | Measurements invalid |
|---|---|---|
| 0 to 30 seconds | send real data, helper not written | nothing sent (grace period) |
| 31 to 60 seconds | send real data, helper written | nothing sent (grace period) |
| more than 60 seconds, or helper empty | send real data, helper written | selected reaction |

The go-eCharger calculates its `pvopt_*` averages from the last values it has received, no matter how old they are. Without the zero values, a car that is (re)connected at night can start charging at sunrise on the basis of the previous day's surplus, even though the PV generation has not started yet.

## go-eCharger Setup

1. Enable **ECO mode** (Logic mode: Awattar [Eco])
2. Enable **"Use PV surplus"** (Mit PV-Überschuss laden)
3. Enable **"Allow Charge Pause"** (Ladepausen zulassen)
4. Set **Grid Target** to negative value (e.g., -500W)

## Testing

The blueprint has automated regression tests in
[`tests/blueprints`](../../../tests/blueprints). They were added together with
the target charger selection and the measurement validation (contributed by
MrCodeLabs) and extended for the reaction to invalid measurements, the battery
option, the grace period, the notifications and the time zone handling.

```sh
python -m pip install -r tests/blueprints/requirements.txt
python -m pytest tests/blueprints -q
```

The tests load the real blueprint YAML, resolve the input defaults, render the
Jinja templates and evaluate the actions (`if`, `choose`, `stop`, conditions)
with synthetic sensor states and entity registries. The routing tests also run
the unchanged `set_pv_data` method of this integration against two simulated
chargers. No hardware, credentials or network are used.

What they cover:

| Area | Examples |
|---|---|
| Target charger | Selected charger gets every update (daylight, night, sunset); mixed chargers, device and area targets, wrong integration and a removed entry are rejected; no fallback to another charger |
| Measurement validation | `unknown`, `unavailable`, text, NaN, infinity and overflow in every used sensor; a real zero is valid; one state read per sensor and tick |
| Grid methods | Single, consumption + feed-in, phases; precedence; incomplete selection; no method selected; more than three phases |
| Units and arithmetic | Multiplier, inversion, rounding after conversion, invalid multiplier |
| Reaction and battery | Zero, notify and keep; battery 0 or treated as invalid; unknown policy value falls back to zero |
| Grace period | Boundary at the grace period; empty, unknown and future helper values; helper write throttling; independent of the time zone of the test process |
| Notifications | Throttled to once a minute, closed again when the problem is gone |
| Night and sunset | Zero values are independent of measurement validity |

Limits: the tests use test doubles for states, registries and the action
evaluator. They do not replace a check in a running Home Assistant. Not
covered are the selector UI, automation traces, behaviour over several ticks in
a real automation, WAN filtering, firmware behaviour and the physical charger.
No claim is made that stopping transmission stops charging. More details are in
[`tests/blueprints/README.md`](../../../tests/blueprints/README.md).

## Troubleshooting

- **No data transmission**: Check entity names and availability, and that the "car connected" entity reports `on`
- **Wrong values**: Use inversion options for incorrect sign conventions
- **Values are 1000 times too small**: Your entities report kW. Set the **Power Unit Multiplier** to `1000`
- **Car starts charging at sunrise before the PV generation has started**: Update to the latest version of the blueprint, which sends zero values at night
- **Charging issues**: Verify go-eCharger ECO mode settings
- **Blueprint not visible**: Ensure HA version ≥ 2024.6.0
- **Zero values are sent in daylight, charging drops to the minimum or stops**: A used sensor is `unavailable`, `unknown` or not numeric, and the default reaction sends zero values. Open the automation trace (*Settings > Automations & Scenes*, the automation, *Traces*) and check the variables `measurements_valid` and `power_samples`: the sensor with a bad value is listed there. Fix the sensor, or add a **Grace period helper** to tolerate short dropouts
- **Nothing is sent in daylight although a car is connected**: Check the reaction setting. With *Keep last values* or *Skip update and notify* an invalid measurement sends nothing. Also check that the trace shows `measurements_valid` as `true`, and that the sun is between sunrise and sunset
- **Persistent notification "invalid measurement"**: The reaction is *Skip update and notify* and a used sensor is invalid. The charger keeps its last values and may charge from the grid. Fix the sensor; the notification closes itself once the data is valid again
- **Persistent notification "invalid target charger"**: The selected **Target go-eCharger** does not match the **Car connected** entities. Select entities that belong to that integration entry, or clear the target. Device and area targets do not work with an explicit target
- **Zero values although all sensors look fine, with the 3-phase method**: The phase method needs at least three distinct entities. With fewer phases (for example a two-phase connection) use a sensor for the total grid power with the *Single Entity* method
- **Zero values although all sensors look fine, with consumption and feed-in**: Both entities must be selected. With only one of them the selection is incomplete and counts as invalid
- **The charger kept charging from the grid during a sensor outage**: The reaction was *Skip update and notify* or *Keep last values*, so the charger worked with its last values. Choose *Send zero values*, and keep a grace period short
- **The grace period reacts earlier than configured**: The reaction starts between half and the full grace period after the last valid measurement, because the helper is refreshed every half grace period
- **The grace period seems to have no effect**: The helper must be of type *Date and time*. A date-only or time-only helper gives a wrong age and is rewritten on every tick. Also check that the reaction is not *Keep last values*, where nothing is sent either way
- **The database grows because of the helper**: Exclude the helper from the recorder, see [Optional grace period](#optional-grace-period)
- **Battery sensor failed and the battery value is 0**: That is the default (*Battery sensor unavailable = Send battery 0*), so charging continues. Switch to *Treat as invalid measurement* if your battery often charges or discharges with high power
- **Warnings "Already running" in the log**: Older versions logged them whenever a slow charger call overran the 5 second tick. The blueprint now sets `max_exceeded: silent`; update to the latest version

## Changelog

### 2026-10-23

**Added**
- New optional input **Target go-eCharger**: all updates (daylight, night, sunset) go to the selected integration entry. Required for more than one charger. Empty keeps the previous default
- New input **Reaction to invalid daylight measurements** (default: send zero values)
- New optional inputs **Grace period helper** and **Grace period (seconds)**
- New input **Battery sensor unavailable** (default: send battery 0)
- Invalid target charger and invalid measurements are reported in a persistent notification, which is closed again once the problem is gone
- Regression tests for the blueprint templates in `tests/blueprints`

**Changed behaviour (upgrade notes)**
- Missing, `unavailable`, `unknown`, non-numeric or non-finite measurements are no longer replaced by 0 inside the calculation. A used grid or PV sensor that is invalid now leads to the selected reaction, by default zero values. Before, the remaining sensors were still sent, for example a missing PV sensor gave `ppv=0` with a real `pgrid`
- A selected but incomplete grid method is invalid and does not fall back to another method. This affects consumption without feed-in (or the other way round), fewer than three phase entities, and duplicate phase entities. Before, `pgrid=0` was sent silently. Use the *Single Entity* method with a total power sensor instead
- Each used sensor state is read once per tick, so validation and calculation use the same values
- An invalid target charger stops the run with a notification instead of an error in the log, and `max_exceeded: silent` avoids an "Already running" warning when a slow charger call overruns the 5 second tick

**Unchanged for complete setups**
With valid measurements the blueprint sends the same values as before, for every grid method. No grid method selected still sends `pgrid=0`, and more than three phase entities still use the first three.

Example (grid consumption 0.2 kW, feed-in 1.0 kW, PV 3.0 kW, battery -0.5 kW, multiplier `1000`), sent as `pgrid / ppv / pakku`:

| Setup | Earlier versions | Now (defaults) |
|---|---|---|
| Consumption + feed-in, all valid | -800 / 3000 / -500 | -800 / 3000 / -500 |
| Single entity, valid | 200 / 3000 / -500 | 200 / 3000 / -500 |
| No grid method selected | 0 / 3000 / -500 | 0 / 3000 / -500 |
| Four phase entities | 300 / 3000 / -500 | 300 / 3000 / -500 |
| Two phase entities | 0 / 3000 / -500 | 0 / 0 / 0 |
| Consumption entity only | 0 / 3000 / -500 | 0 / 0 / 0 |
| Feed-in sensor `unavailable` | 200 / 3000 / -500 | 0 / 0 / 0 |
| PV sensor `unavailable` | -800 / 0 / -500 | 0 / 0 / 0 |
| Battery sensor `unavailable` | -800 / 3000 / 0 | -800 / 3000 / 0 |

The last four rows differ because a missing measurement is no longer treated
as a real zero. With *Keep last values* nothing is sent in these cases.

### 2026-09-30
- Send zero values at sunset and every 30 seconds at night while a car is connected
- New input **Power Unit Multiplier** (default `1`, backward compatible)
- Rounding now happens after the multiplication
- The "car connected" condition works with string and list target values
- README: file name in the manual installation corrected

## Support

For issues with the blueprint, please create an issue in this repository.
For go-eCharger integration issues, see the [main integration documentation](../../../README.md).
