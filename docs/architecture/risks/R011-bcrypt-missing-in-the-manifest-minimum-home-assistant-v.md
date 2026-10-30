---
id: R011
date: 2026-10-27
category: INT
probability: 3
impact: 3
residual_probability: 1
residual_impact: 3
strategy: mitigate
status: settled
owner:
review: release
---
# R011: `bcrypt` missing in the manifest, minimum Home Assistant version unclear

## Risk description

If the integration is installed on an older Home Assistant or without an available `bcrypt`, then dependencies or APIs are missing, which means installation or start fails.

## Finding in detail

**Finding.** Two parts. (1) `bcrypt` is imported (`pygoecharger_ha/__init__.py`, line 15) but not named in the manifest. (2) `hacs.json` names Home Assistant 2023.8.0 as the minimum, but the config flow calls `self._get_reconfigure_entry()` (`config_flow.py`, lines 156 and 226).

**Effect.** (1) None: Home Assistant itself requires `bcrypt` (the version installed for the tests pins `bcrypt==5.0.0` and uses it in its own auth provider), and the maintainer removed it from the manifest because Home Assistant complained that it was declared (review of this pull request, 2026-10-30). (2) [Inference] Reconfiguring an entry fails with an `AttributeError` on Home Assistant older than 2024.11.0, because `_get_reconfigure_entry` is missing in 2024.10.4 and present in 2024.11.0 (checked in the released packages). Not run on an old system.

## Assessment

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Assessment | 3 | 3 | 9 | medium |
| Residual risk after the countermeasure | 1 | 3 | 3 | low |

Risk strategy: **Mitigate**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.
<!-- /risk:assessment -->

## Countermeasure

Part 1 is obsolete: nothing to add to the manifest. Part 2: raise the minimum in `hacs.json` to 2024.11.0, or guard the call. Proposal for the maintainer, not implemented. The tests run with the newest version only. Other newer APIs were not checked one by one.

## Status and history

<!-- risk:status -->
Closed (settled, not a defect)
<!-- /risk:status -->

Settled on 2026-10-30 after the review of the maintainer: the `bcrypt` part is not a defect. The original assessment (W 3, A 3) is kept. Residual risk: the minimum version in `hacs.json` is too low for the reconfigure flow (W 3, A 1 [Inference]: only reconfiguring is affected). It is recorded here and accepted until the maintainer decides about `hacs.json`.

## Evidence

*Evidence at the time of the finding (not today's state)*

[Code] `manifest.json` (`requirements`: only `msgpack`), `pygoecharger_ha/__init__.py` line 15, `config_flow.py` lines 156 and 226. [Docs] The Home Assistant package installed for the tests requires `bcrypt==5.0.0` (package metadata) and imports it in `auth/providers/homeassistant.py`. [Code] `config_entries.py` of the released packages 2024.10.4 (no `_get_reconfigure_entry`) and 2024.11.0 (present). Not tried on an old Home Assistant.  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Inference]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../arc42-ha-goecharger-api2.md) | [Back to the register](README.md)
