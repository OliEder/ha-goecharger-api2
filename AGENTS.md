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
- Write code comments, commit messages and pull request text in English.
- Do not log or store tokens and passwords (not in logs, device info, tests or documents).
- No blocking input or output in the event loop (the integration is asynchronous).

## Known pitfalls

These classes of defects were found in this code base (see the risk register). Check them before you change the related code.

- **Two data paths.** The WebSocket path and the HTTP path return different results for the same write (an empty `{}` or a dict with the value) and are changed separately: [R027](docs/architecture/risks/R027-false-error-after-a-successful-multiple-write.md), [R001](docs/architecture/risks/R001-stop-charging-locks-the-charger-after-a-write-error.md), [R004](docs/architecture/risks/R004-error-handling-for-multiple-writes-calls-the-wrong-sign.md). Test a change on both paths (`test_versions_transport_parity.py` is an example).
- **Chargers and controllers.** A controller has no `tcl` and no `cll`. Code that reads or writes a key must not assume it exists ([R029](docs/architecture/risks/R029-without-cablecurrentlimit-there-is-no-limit-to-16-a-any.md), #177). Check the key table of the device type.
- **Several chargers in one Home Assistant.** State per entry (service registry, counters) is added and removed per entry ([R002](docs/architecture/risks/R002-multi-charger-registry-incomplete.md), [R003](docs/architecture/risks/R003-active-charger-counter-with-controller-entries.md)). Without `configid` a service call is refused when more than one charger exists (ADR-0010).
- **Broad `except`.** `except BaseException` also catches cancellation and replaces a specific message by a general one ([R025](docs/architecture/risks/R025-specific-start-error-message-is-covered-up.md)). Catch what you can handle.
- **Values from callers are not trusted.** Check numbers for finiteness (`NaN`, `inf`) before they go to a charger ([R005](docs/architecture/risks/R005-pgrid-without-a-finiteness-check.md)).
- **Settings survive a restart.** A value the user set must still be there after a restart ([R030](docs/architecture/risks/R030-max-ampere-is-reset-at-every-restart.md), reported by the maintainer, not yet reproduced).

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
- A Home Assistant API that is newer than the minimum version in `hacs.json` ([R011](docs/architecture/risks/R011-bcrypt-missing-in-the-manifest-minimum-home-assistant-v.md)).
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
- Use invented test data (serial `123456`, address `192.0.2.10`), never a real serial number, token or address.
- All tests run with fakes and say nothing about the real charger. Say so where it matters.

## Findings need evidence and a risk

Before you report anything, look at the risk register (`docs/architecture/risks/`), the decisions (`docs/architecture/adr/`) and the open and closed issues. If the behaviour is already listed, or marked as intended, do not report it again.

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

- **Start from the current `main`**, on a branch of your fork. **One topic per pull request.** General infrastructure goes into its own pull request, apart from the feature that needs it.
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

Everything below is a summary for agents without Superpowers. It follows the three skills closely (MIT licence, by Jesse Vincent), leaves out their examples, and each part ends with the source. **If you can read URLs, read the full skill before you start work of that kind. If you cannot, the summary here is enough.**

### Test first (summary of `test-driven-development`)

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

- **Red.** Write one minimal test for one behaviour, with a name that says what should happen. Use real code; mock only what you cannot avoid. Run it and confirm that it *fails* (not errors), with the message you expect, because the behaviour is missing and not because of a typo. A test that passes at once tests existing behaviour: fix the test.
- **Green.** Write the simplest code that passes. Add no feature, no refactoring of other code, no improvement beyond the test. Run it and confirm: the test passes, the other tests of the project still pass (the whole suite, not only your file), the output is clean. **If a test fails, fix the code, not the test.** Name every failure that run shows, also one you did not cause.
- **Refactor.** Only after green: remove duplication, improve names, extract helpers. Add no behaviour. Keep it green.
- **Bug fix.** Write a failing test that reproduces the bug first. Never fix a bug without one.
- **Code that exists before its test is deleted**, not kept as a reference and not adapted while writing the test. Implement it again from the test.
- **Excuses that all mean "test first":** too simple to test, I will test after, tests after achieve the same, I tested it by hand, deleting my work is wasteful, keep it as a reference, I need to explore first, the test is hard to write (then the design is unclear), TDD is dogmatic, this case is different. If you notice one, stop and start over with the test.
- **Done only when:** every new behaviour has a test, you watched each test fail first for the expected reason, you wrote minimal code, all tests pass with clean output, edge cases and errors are covered.

Source: <https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md>

### Systematic debugging (summary of `systematic-debugging`)

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Apply it to every failure, bug or unexpected behaviour, above all when you are in a hurry, when a quick fix looks obvious, or when an earlier fix did not work. Finish each phase before the next.

1. **Find the root cause.** Read error messages and stack traces completely. Reproduce the problem reliably; if you cannot, gather more data and do not guess. Check what changed recently (diff, commits, dependencies, configuration). Where several components are involved (here: entity, coordinator, bridge, device), log what enters and leaves each boundary and find out where it breaks before you fix anything. Trace a bad value back to where it comes from and fix it there, not at the symptom.
2. **Find the pattern.** Find similar working code in the same code base and compare it with the broken code. List every difference, however small, and the dependencies and assumptions involved.
3. **Test one hypothesis.** State it ("I think X is the cause because Y"), make the smallest change that tests it, change one variable at a time. If it did not work, form a new hypothesis; do not stack fixes. If you do not understand something, say so.
4. **Fix.** Write the failing test first, make one change for the root cause, no "while I am here" improvements, then verify the fix and that nothing else broke. **If three fixes failed, stop and question the design with the maintainer before you try a fourth.**

Source: <https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md>

### Verification before completion (summary of `verification-before-completion`)

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

Before you say that something is done, fixed or passing (and before you commit or open a pull request): **identify** the command that proves the claim, **run** it completely and freshly, **read** the whole output, the exit code and the number of failures, and only then **state** the result together with the evidence. If the output does not confirm the claim, report the real status.

| Claim | Needs | Not enough |
|---|---|---|
| Tests pass | the test command shows 0 failures | an earlier run, "should pass" |
| Bug fixed | the test of the original symptom passes | the code was changed |
| Regression test works | red-green verified: passes, fix reverted, **fails**, fix restored, passes | it passed once |
| Delegated work is done | the diff shows the changes | the other agent reports success |
| Requirements met | a line-by-line check against the requirements | the tests pass |

"Should", "probably" and "seems" are warning signs, as is any expression of satisfaction before the check ("Done!"). The rule covers paraphrases and implications too.

Source: <https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md>
