---
id: R12
date: 2026-10-27
category: INT
probability: 3
impact: 2
residual_probability: 2
residual_impact: 2
strategy: mitigate
status: open
owner:
review: release
---
# R12: `CustomFriendlyNameEntity` überschreibt eine private HA-Methode

## Risikobeschreibung

Wenn Home Assistant die private Methode `_Entity__async_calculate_state` ändert, dann greift die Überschreibung ins Leere oder wirft einen Fehler, was dazu führt, dass Anzeigenamen falsch sind oder Entitäten ausfallen.

## Befund im Detail

**Befund.** `CustomFriendlyNameEntity` überschreibt eine private HA-Methode.

**Wirkung.** Bricht bei HA-Änderungen.

## Bewertung

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Bewertung | 3 | 2 | 6 | mittel |
| Restrisiko nach der Gegenmaßnahme | 2 | 2 | 4 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.
<!-- /risk:assessment -->

## Gegenmaßnahme

Die Tests gegen neue Home-Assistant-Versionen laufen lassen, um Brüche früh zu sehen (die Version des Test-Frameworks steht in `requirements_dev.txt`). Eine eigene Absicherung der Überschreibung gibt es nicht.

## Status und Verlauf

<!-- risk:status -->
Offen
<!-- /risk:status -->

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Aus Code gelesen.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
