---
id: R021
date: 2026-10-29
category: ARCH
probability: 2
impact: 3
residual_probability: 1
residual_impact: 3
strategy: mitigate
status: open
owner:
review: release
---
# R021: Migration from 2.0 to 2.1 deletes all devices

## Risk description

If an entry of version 2.0 is migrated, then `async_migrate_entry` deletes all devices of the entry and thus probably the entries of the entity registry, which means customised names, areas and enabled entities are lost.

## Finding in detail

**Finding.** The migration from 2.0 to 2.1 deletes **all devices** of the entry (`async_remove_device`, `__init__.py`, lines 86 to 94). Home Assistant thereby also removes every entity registry entry of that device, including disabled ones (`async_device_modified` in `helpers/entity_registry.py`, Home Assistant 2026.10.4).

**Effect.** Names, areas, labels, renamed entity IDs and manually enabled entities (many sensors are off by default) adjusted by users are lost and must be set again. Default entity IDs stay the same because the code builds them from the serial number and the key (`__init__.py`, lines 908 and 910); an entity ID the user renamed is not kept.

## Assessment

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Assessment | 2 | 3 | 6 | medium |
| Residual risk after the countermeasure | 1 | 3 | 3 | low |

Risk strategy: **Mitigate**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.
<!-- /risk:assessment -->

## Countermeasure

The migration should not delete devices. Removing the purge alone would leave the old identifiers, which for cloud entries contained the token ([R022](R022-version-1-entries-leave-old-devices-in-the-registry.md)); the identifiers should be rewritten instead. Entity IDs that users customised are lost as well. `async_migrate_entry` catches `BaseException` and the version is bumped anyway, so a failed purge is not repeated. The case now concerns only entries still on 2.0. The HA behaviour is assumed from memory and not replayed.

## Status and history

<!-- risk:status -->
Open
<!-- /risk:status -->

## Evidence

*Evidence at the time of the finding (not today's state)*

[Code] `__init__.py` lines 86 to 94; `helpers/entity_registry.py` of Home Assistant 2026.10.4 (the installed test version). [Test] Replayed on 2026-10-30 with real registries in a throw-away test (not added to the suite): an entity renamed to `sensor.my_wallbox_power` with a custom name was gone from the entity registry after `async_migrate_entry` on a 2.0 entry, and the entry stood at version 2.1. Not tried in a running Home Assistant and not with older versions.  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Inference]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../arc42-ha-goecharger-api2.md) | [Back to the register](README.md)
