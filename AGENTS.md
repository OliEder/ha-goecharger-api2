# AGENTS.md

Instructions for AI coding agents (Claude Code, Codex, Copilot and similar) working on this repository. The maintainer decides what goes in, and a human reviews every change. If a rule here is wrong or in your way, say so and let the maintainer change this file.

## Project overview

`goecharger_api2` ("go-e APIv2 Connect") is a Home Assistant custom integration (HACS) for go-eCharger wallboxes and the go-eController. It talks to the device over a local WebSocket (when a password is set), local HTTP polling, or the go-e cloud.

- Python, asynchronous (`asyncio`, `aiohttp`). Domain `goecharger_api2`, version in `custom_components/goecharger_api2/manifest.json`.
- Supports Home Assistant 2023.8.0 or newer (`hacs.json`). The tests run against one pinned, recent Home Assistant (`requirements_dev.txt`).
- The WebSocket interface is not officially documented. The official API tables are the reference for keys: <https://github.com/goecharger/go-eCharger-API-v2>.

## Commands

```bash
python3.14 -m venv .venv && . .venv/bin/activate        # Python 3.14 is required by the test framework
python -m pip install -r requirements_dev.txt

python -m pytest tests/integration -m "not known_bug and not needs_decision"   # blocking set, must be green
python -m pytest tests/integration -m "known_bug or needs_decision"            # open findings, red on purpose
python tests/tools/build_risk_register.py --check                              # risk documents match their front matter
```

CI (`.github/workflows`): hassfest, HACS validation, `tests.yaml` (the first two commands above). Details in `tests/integration/README.md` and `tests/tools/README.md`.

## Project structure

| Path | What it is |
|---|---|
| `custom_components/goecharger_api2/__init__.py` | Setup, `GoeChargerDataUpdateCoordinator`, base entity |
| `.../pygoecharger_ha/__init__.py` | Bridge: HTTP, cloud and WebSocket (login, messages, writes) |
| `.../pygoecharger_ha/keys.py` | `Tag`: every API key with its flags |
| `.../pygoecharger_ha/const.py` | Key filters per read cycle, texts, enums |
| `.../const.py` | Entity descriptions per platform, for chargers and for controllers |
| `.../sensor.py`, `number.py`, `select.py`, `switch.py`, `button.py`, `binary_sensor.py` | One generic entity class per platform |
| `.../service.py`, `services.yaml` | The services (`set_pv_data`, `stop_charging`, ...) |
| `.../config_flow.py` | Setup and reconfiguration dialog |
| `.../translations/` | `de.json`, `en.json`, `fr.json` |
| `example/blueprint/` | The PV surplus blueprint |
| `tests/integration/` | Regression tests (`contract/` holds the official key tables) |
| `tests/tools/` | Report, risk register and site tools |
| `docs/architecture/` | arc42, risk register (`risks/`), decisions (`adr/`) |
| `docs/quality/` | Test concept |

## Code style

- There is no formatter or linter configured. **Match the surrounding code**: naming, comment density, `_LOGGER` levels, f-strings, 4 spaces. Do not reformat lines you do not change.
- New entities and keys go into the existing mechanisms: a `Tag` in `keys.py`, an entity description in `const.py`, the read filter in `pygoecharger_ha/const.py`, texts in all three translation files.
- Do not log or store tokens and passwords (not in logs, device info, tests or documents).

## Boundaries

**Always**
- Write the failing test first (see "Testing").
- Run the blocking set before you say a change is done, and name every failure it shows, also one you did not cause.
- Name the source of a claim (file and line, or the official documentation) and say what was *not* tried on a real device.
- Update the documentation the change touches (see "Documentation").
- Say in the pull request that an AI agent helped.

**Ask first**
- Behaviour that looks like a bug but may be intended (for example keeping the last values when a read fails, #173).
- A new file or module, a new dependency, `manifest.json`, `hacs.json`, the minimum Home Assistant version, or a version number.
- Anything that changes entity IDs or `unique_id`s (existing users would lose their entities; `test_entity_ids.py` guards this).
- Removing or renaming a service, an option or a key.
- Anything that writes to a real charger.

**Never**
- Change a test only to make it pass, or hide a failure with `skip`, `xfail` or a marker.
- Add `if new_tag: ... else: ...` branches to the platforms, or a new Python file for a single feature.
- Open a pull request, comment or issue without a human's go-ahead.
- Copy a password or token from a config entry into code, tests, documents, issues or pull requests.
- Edit the generated blocks between `<!-- risk:... -->` markers by hand.
- Add long generated documentation. Update a document that exists instead.

## Testing

- **A test comes from something outside the code under test:** the official go-e API tables, the Modbus profile, an observed device answer, a decision of the maintainer. A test that only repeats what generated code does proves nothing.
- **When a test fails, change the code, not the test.** A test changes only when the requirement changed (maintainer, official documentation, observed device answer); the pull request says which.
- **The markers are for findings.** A known defect gets a test marked `known_bug`, a deviation that needs the maintainer's decision gets `needs_decision`. Remove the marker in the same change that fixes the defect.
- All tests run with fakes and say nothing about the real charger. Say so where it matters.

## Findings need evidence and a risk

Do not report "this is a bug" without:

- **Where:** file and line, or the quoted line of the official documentation.
- **What was checked:** the test that shows it (name), or the reading of code or documentation. Mark the level `[Code]`, `[Docs]` or `[Inference]`.
- **What was not tried:** for example "not tried on a real charger".
- **Its risk:** an entry in `docs/architecture/risks/`. Copy a neighbouring file, fill the front matter (probability and impact 1 to 5, residual values, strategy, status) and write the "if cause, then event, which leads to impact" sentence. Run `python tests/tools/build_risk_register.py`; it writes the tables, heat maps and links. When the risk is fixed, close the entry and name the commit.

Probability, impact and strategy are assessments. Mark them as such until the maintainer confirms them. Report findings as short, concrete points.

## Documentation

Update only what the change touches:

| If the change ... | update |
|---|---|
| is visible to users (services, entities, options) | `README.md`, `docs/PVSURPLUS.md`, `services.yaml`, the translations |
| changes how the integration works (flows, building blocks, interfaces) | `docs/architecture/arc42-ha-goecharger-api2.md` (and its diagrams) |
| decides something with consequences (new default, removed option, changed behaviour) | a new record in `docs/architecture/adr/` (copy the last one, next number, update the index) |
| adds, changes or closes a risk | `docs/architecture/risks/` |
| adds tests or changes their rules | `docs/quality/testkonzept-ha-goecharger-api2.md` (numbers and the risk coverage table) |

## Commits and pull requests

- **One topic per pull request.** General infrastructure goes into its own pull request, apart from the feature that needs it.
- Commit subject: short and in the imperative, for example `fix: stop_charging resets _stop_in_progress after a failed write`. Existing history is informal, so what matters is that it says what changed.
- The pull request says what changed and why, what was tested and what was not (no real charger), and which documents were updated.
- Do not mix reformatting with a change.

## Use the Home Assistant MCP server

An integration behaves as it does inside a real Home Assistant, not as the code suggests. **Use a Home Assistant MCP server whenever one is available** (for example the community project `ha-mcp`, or the MCP server integration of Home Assistant itself) instead of guessing.

- Use it to read entity states and attributes of this integration, check the entity registry (entities disabled by default, `unique_id`, names), read the log to confirm or refute an `ERROR` or warning, and look at the config entry and the registered services.
- **Read first.** Call services or write settings only on a test instance, or with the explicit consent of the owner of the device. A real charger is not a test bench.
- State in the report what was read from a real instance and what was not.

## Stop here if you already use Superpowers

If your agent already works with [Superpowers](https://github.com/obra/superpowers) (the skills `test-driven-development`, `systematic-debugging` and `verification-before-completion` are loaded), **you do not need to read on.** Follow the rules of those skills; everything above is the project-specific part and applies in addition.

Everything below is a short summary for agents without Superpowers. It is adapted from the Superpowers skills (MIT licence), which are the full reference:

- [`test-driven-development`](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md)
- [`systematic-debugging`](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md)
- [`verification-before-completion`](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md)

### Test first, in short

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

1. **Red:** write one small test for one behaviour. Run it and watch it fail, for the right reason (the behaviour is missing, not a typo). A test that passes at once tests existing behaviour.
2. **Green:** write the least code that makes it pass. Run the whole blocking set.
3. **Refactor:** clean up while everything stays green. Add no behaviour.
4. A bug fix starts with a test that reproduces the bug. Never fix a bug without one.
5. Code written before its test is deleted and written again from the test.

"Too simple to test", "I will test after", "I tested it by hand", "deleting my work is wasteful", "the test is wrong, I will adjust it": all of these mean the test comes first, or that you show evidence for the change of the test. If you notice one of them, start over.

### Debugging and finishing, in short

- Find the cause before you change code. Reproduce, read the error, check what changed. A guess is not a fix.
- Do not say "done" or "fixed" before you have run the check that proves it and read its output.
