---
id: R21
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
# R21: Migration von 2.0 auf 2.1 löscht alle Geräte

## Risikobeschreibung

Wenn ein Entry der Version 2.0 migriert wird, dann löscht `async_migrate_entry` alle Geräte des Entries und damit vermutlich die Einträge der Entity-Registry, was dazu führt, dass angepasste Namen, Bereiche und aktivierte Entitäten verloren gehen.

## Befund im Detail

**Befund.** Die Migration von 2.0 auf 2.1 löscht **alle Geräte** des Entries (`async_remove_device`). HA entfernt damit nach meinem Wissen auch die zugehörigen Einträge der Entity-Registry.

**Wirkung.** Von Nutzern angepasste Namen, Bereiche, Beschriftungen und manuell aktivierte Entitäten (viele Sensoren sind standardmäßig aus) gehen vermutlich verloren und müssen neu gesetzt werden. Die Entity-IDs bleiben gleich, da sie im Code erzeugt werden.

## Bewertung

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Bewertung | 2 | 3 | 6 | mittel |
| Restrisiko nach der Gegenmaßnahme | 1 | 3 | 3 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.
<!-- /risk:assessment -->

## Gegenmaßnahme

Die Migration soll Geräte nicht löschen. Der Fall betrifft nur noch Entries, die noch auf 2.0 stehen. Das HA-Verhalten ist aus dem Gedächtnis angenommen und nicht nachgespielt.

## Status und Verlauf

<!-- risk:status -->
Offen
<!-- /risk:status -->

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

HA-Verhalten aus dem Gedächtnis, im Code nur der Aufruf belegt. **Nicht nachgespielt.**  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
