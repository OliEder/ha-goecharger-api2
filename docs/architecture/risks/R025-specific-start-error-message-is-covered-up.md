---
id: R25
date: 2026-10-29
category: ARCH
probability: 3
impact: 1
residual_probability: 1
residual_impact: 1
strategy: mitigate
status: fixed
owner:
review: release
---
# R25: Konkrete Startfehlermeldung wird überdeckt

## Risikobeschreibung

Wenn beim Start keine Gerätedaten verfügbar sind, dann ersetzt `except BaseException` die konkrete Meldung durch die allgemeine WebSocket-Meldung, was dazu führt, dass Nutzer eine unpassende Fehlermeldung sehen.

## Befund im Detail

**Befund.** `async_setup_entry`: Die Meldung „could not fetch essential information“ wird innerhalb eines `try` erzeugt und von `except BaseException` sofort durch die allgemeine WebSocket-Meldung ersetzt.

**Wirkung.** Nutzer sehen eine unpassende Fehlermeldung.

## Bewertung

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Bewertung | 3 | 1 | 3 | niedrig |
| Restrisiko nach der Gegenmaßnahme | 1 | 1 | 1 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.
<!-- /risk:assessment -->

## Gegenmaßnahme

Die konkrete `ConfigEntryNotReady`-Meldung bleibt erhalten (`eb5da46`).

## Status und Verlauf

<!-- risk:status -->
Geschlossen (behoben)
<!-- /risk:status -->

`eb5da46`. Seit `eb5da46` bleibt die konkrete `ConfigEntryNotReady`-Meldung erhalten.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Im Test gezeigt (`known_bug`).  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
