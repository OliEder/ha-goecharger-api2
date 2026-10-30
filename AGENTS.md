# AGENTS.md

Rules for AI coding agents (Claude Code, Codex, Copilot and similar) that work on this repository. The maintainer decides what goes in; a human reviews every change. If a rule here is wrong or in your way, say so and let the maintainer change this file.

## 1. Ground rules (from the maintainer, see issues #172, #173, #177)

1. **Use AI sparingly and say so.** Do not use an agent for what a person can check in a few minutes. If an agent helped, the pull request says so.
2. **One topic per change.** General infrastructure goes into its own pull request, apart from the feature that needs it.
3. **Follow the existing structure.** Reuse the entity descriptions in `const.py` and the existing tag mechanism. No new Python file for a single feature. No `if new_tag: ... else: ...` branches in the platforms, they pile up with every new tag.
4. **Do not guess, check.** Before claiming that a device supports a key (for example `tcl` on a controller), read the official key table or the code and name the source. Say what was *not* tried on a real device.
5. **Intentions of the maintainer win.** If something looks like a bug but may be intended (for example keeping the last values when a read fails, #173), ask first; do not "fix" it.
6. **No walls of text.** Documentation is short and concrete. Update an existing document instead of adding a new one. No generated prose for its own sake.
7. **Nothing leaves the machine without a human's go-ahead.** No pull request, comment or issue is opened by an agent on its own.

## 2. Work test-first (TDD, as in Superpowers)

```
No production code without a failing test first.
```

1. **Red:** write one small test for one behaviour. Run it and watch it fail, for the right reason (the behaviour is missing, not a typo).
2. **Green:** write the least code that makes it pass. Run the whole blocking set.
3. **Refactor:** clean up while everything stays green. Add no behaviour.
4. **A bug fix starts with a test that reproduces the bug.** Never fix a bug without one.
5. Code written before its test is thrown away and written again from the test.

Where the tests come from matters: **a test must be derived from something outside the code under test** (the official go-e API tables, the Modbus profile, an observed device answer, a decision of the maintainer). A test that only repeats what the generated code does proves nothing.

How to run (details in `tests/integration/README.md`):

```
python -m pytest tests/integration -m "not known_bug and not needs_decision"   # blocking set, must be green
python -m pytest tests/integration -m "known_bug or needs_decision"            # open findings, red on purpose
```

A known defect gets a test marked `known_bug`, a deviation that needs the maintainer's decision `needs_decision`. When the defect is fixed, remove the marker in the same change. All tests run with fakes and say nothing about the real charger; say so where it matters.

## 3. A finding needs evidence, and a risk

Do not report "this is a bug" without all of the following:

- **Where:** file and line, or the quoted line of the official documentation.
- **What was checked:** the test that shows it (name), or the reading of code or documentation. Mark the level: `[Code]`, `[Docs]` or `[Inference]` (the marks used in the arc42 document).
- **What was not tried:** for example "not tried on a real charger".
- **Its risk:** an entry in the risk register, `docs/architecture/risks/`. Copy a neighbouring file, fill the front matter (probability and impact 1 to 5, residual values, strategy, status) and write the "if cause, then event, which leads to impact" sentence. Then run `python tests/tools/build_risk_register.py`: it writes the tables, the heat maps and the links. When the risk is fixed, close the entry and name the commit.

Probability, impact and strategy are assessments. Mark them as such until the maintainer confirms them.

## 4. Keep the documentation in step

Before a change is done, check each of these and update only what the change touches:

| If the change ... | update |
|---|---|
| is visible to users (services, entities, options) | `README.md`, `docs/PVSURPLUS.md`, `services.yaml` and the translations |
| changes how the integration works (flows, building blocks, interfaces) | `docs/architecture/arc42-ha-goecharger-api2.md` (and its diagrams) |
| decides something with consequences (new default, removed option, changed behaviour) | a new record in `docs/architecture/adr/` (copy the last one, next number, update the index) |
| adds, changes or closes a risk | `docs/architecture/risks/` (see section 3) |
| adds tests or changes their rules | `docs/quality/testkonzept-ha-goecharger-api2.md` (numbers and the risk coverage table) |

CI checks the generated parts of the risk documents (`python tests/tools/build_risk_register.py --check`). Do not edit the blocks between `<!-- risk:... -->` markers by hand.

## 5. Use the Home Assistant MCP server

An integration behaves as it does inside a real Home Assistant, not as the code suggests. **Agents should use a Home Assistant MCP server whenever one is available** (for example the community project `ha-mcp`, or the MCP server integration of Home Assistant itself) instead of guessing.

Use it to:

- read entity states and attributes of this integration and check the entity registry (entities that are disabled by default, `unique_id`, names),
- read the Home Assistant log to confirm or refute an `ERROR` or a warning,
- look at the config entry of a device (type, mode, options) and at the registered services.

Rules for this:

- **Read first.** Call services or write settings only on a test instance, or with the explicit consent of the owner of the device. A real charger is not a test bench.
- Config entries contain the device password and the cloud token. **Never copy them** into a test, a document, an issue or a pull request.
- State in the report what was read from a real instance and what was not.
