---
id: R3
date: 2026-10-27
category: ARCH
probability: 2
impact: 3
residual_probability: 1
residual_impact: 3
strategy: mitigate
status: fixed
owner:
review: release
---
# R3: Zähler der aktiven Charger bei Controller-Entries

## Risikobeschreibung

Wenn ein Controller-Entry entladen wird, dann senkt der Code den Zähler `ACTIVE_CHARGER_COUNTER`, den nur Charger erhöht haben, was dazu führt, dass die Charger-Dienste verschwinden oder ein `KeyError` auftritt.

## Befund im Detail

**Befund.** `async_unload_entry`: `ACTIVE_CHARGER_COUNTER` wird nur für Charger erhöht, aber für jeden Entry verringert und danach ohne Absicherung gelesen. Bei einem reinen Controller-Entry fehlt der Schlüssel.

**Wirkung.** Mögliche `KeyError` beim Entladen oder falscher Zählerstand bei gemischten Entries.

## Bewertung

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Bewertung | 2 | 3 | 6 | mittel |
| Restrisiko nach der Gegenmaßnahme | 1 | 3 | 3 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.
<!-- /risk:assessment -->

## Gegenmaßnahme

Zähler und Dienste werden nur noch für Charger angepasst (`eb5da46`).

## Status und Verlauf

<!-- risk:status -->
Geschlossen (behoben)
<!-- /risk:status -->

`eb5da46`. Seit `eb5da46` werden Zähler und Dienste nur für Charger angepasst.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Aus Code gelesen (`__init__.py:148`ff, `194`ff). **Nicht nachgespielt.**  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
