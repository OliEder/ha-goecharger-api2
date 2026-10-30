# AGENTS.md

Rules for AI coding agents (Claude Code, Codex, Copilot and similar) that work on this repository. The maintainer decides what goes in, and a human reviews every change. If a rule here is wrong or in your way, say so and let the maintainer change this file.

Read sections 1 to 6: they are specific to this project. **Section 7 is the stop point.**

## 1. Ground rules (from the maintainer, see issues #172, #173, #177)

1. **Use AI sparingly and say so.** Do not use an agent for what a person can check in a few minutes. If an agent helped, the pull request says so.
2. **One topic per change.** General infrastructure goes into its own pull request, apart from the feature that needs it.
3. **Follow the existing structure.** Reuse the entity descriptions in `const.py` and the existing tag mechanism. No new Python file for a single feature. No `if new_tag: ... else: ...` branches in the platforms, they pile up with every new tag.
4. **Do not guess, check.** Before claiming that a device supports a key (for example `tcl` on a controller), read the official key table or the code and name the source. Say what was *not* tried on a real device.
5. **The maintainer's intentions win.** If something looks like a bug but may be intended (for example keeping the last values when a read fails, #173), ask first. Do not "fix" it.
6. **No walls of text.** Documentation is short and concrete. Update an existing document instead of adding a new one.
7. **Nothing leaves the machine without a human's go-ahead.** No pull request, comment or issue is opened by an agent on its own.

## 2. Tests in this repository

```
python -m pytest tests/integration -m "not known_bug and not needs_decision"   # blocking set, must be green
python -m pytest tests/integration -m "known_bug or needs_decision"            # open findings, red on purpose
```

Details are in `tests/integration/README.md`.

- **A test comes from something outside the code under test:** the official go-e API tables, the Modbus profile, an observed device answer, a decision of the maintainer. A test that only repeats what generated code does proves nothing.
- **The markers are for findings.** A known defect gets a test marked `known_bug`, a deviation that needs the maintainer's decision gets `needs_decision`. Never use a marker (or `skip`, `xfail`) to hide a failure of your own change. When a defect is fixed, remove its marker in the same change.
- **When a test fails, change the code, not the test.** A test changes only when the requirement changed (maintainer, official documentation, observed device answer), and the pull request says which.
- **Run the whole blocking set before you call a change done and name every failure** it shows, including one you did not cause.
- All tests run with fakes and say nothing about the real charger. Say so where it matters.

## 3. A finding needs evidence, and a risk

Do not report "this is a bug" without all of the following:

- **Where:** file and line, or the quoted line of the official documentation.
- **What was checked:** the test that shows it (name), or the reading of code or documentation. Mark the level: `[Code]`, `[Docs]` or `[Inference]` (the marks used in the arc42 document).
- **What was not tried:** for example "not tried on a real charger".
- **Its risk:** an entry in `docs/architecture/risks/`. Copy a neighbouring file, fill the front matter (probability and impact 1 to 5, residual values, strategy, status) and write the "if cause, then event, which leads to impact" sentence. Then run `python tests/tools/build_risk_register.py`: it writes the tables, the heat maps and the links. When the risk is fixed, close the entry and name the commit.

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

Use it to read entity states and attributes of this integration, check the entity registry (entities disabled by default, `unique_id`, names), read the Home Assistant log to confirm or refute an `ERROR` or warning, and look at the config entry of a device and the registered services.

- **Read first.** Call services or write settings only on a test instance, or with the explicit consent of the owner of the device. A real charger is not a test bench.
- Config entries contain the device password and the cloud token. **Never copy them** into a test, a document, an issue or a pull request.
- State in the report what was read from a real instance and what was not.

## 6. Reports

Report findings as short, concrete points: file, line, what was checked, what was not tried on a real device.

## 7. Stop here if you already use Superpowers

If your agent already works with [Superpowers](https://github.com/obra/superpowers) (the skills `test-driven-development`, `systematic-debugging` and `verification-before-completion` are loaded), **you do not need to read on.** Follow the rules of those skills; sections 1 to 6 above are the project-specific part and apply in addition.

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

"Too simple to test", "I will test after", "I tested it by hand", "deleting my work is wasteful", "the test is wrong, I will adjust it": all of these mean the test comes first, or that you show evidence for the change of the test (section 2). If you notice one of them, start over.

### Debugging and finishing, in short

- Find the cause before you change code. Reproduce, read the error, check what changed. A guess is not a fix.
- Do not say "done" or "fixed" before you have run the check that proves it and read its output.
