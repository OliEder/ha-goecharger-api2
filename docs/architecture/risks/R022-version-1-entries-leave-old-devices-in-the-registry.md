---
id: R22
date: 2026-10-29
category: MAINT
probability: 1
impact: 1
residual_probability: 1
residual_impact: 1
strategy: accept
status: open
owner:
review: release
---
# R22: Version-1-Entries lassen alte Geräte in der Registry

## Risikobeschreibung

Wenn ein Entry der Version 1 direkt auf 2.1 migriert wird, dann überspringt die Migration das Löschen der Geräte und die Aufräumfunktion existiert nicht mehr, was dazu führt, dass alte Geräte mit dem früheren Identifier in der Registry bleiben.

## Befund im Detail

**Befund.** Entries mit Version 1 werden direkt auf 2.1 migriert und überspringen das Löschen der Geräte. Die alte Aufräumfunktion `check_device_registry` wurde entfernt.

**Wirkung.** Alte Geräte mit dem früheren Identifier (der bei Cloud-Entries den Token enthielt) bleiben dort in der Registry stehen. Sehr seltener Randfall.

## Bewertung

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Bewertung | 1 | 1 | 1 | niedrig |
| Restrisiko nach der Gegenmaßnahme | 1 | 1 | 1 | niedrig |

Risikostrategie: **Akzeptieren**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.
<!-- /risk:assessment -->

## Gegenmaßnahme

Akzeptiert: sehr seltener Randfall.

## Status und Verlauf

<!-- risk:status -->
Offen
<!-- /risk:status -->

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Aus Diff gelesen.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
