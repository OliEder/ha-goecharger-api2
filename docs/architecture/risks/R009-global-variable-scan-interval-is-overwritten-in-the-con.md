---
id: R9
date: 2026-10-27
category: MAINT
probability: 2
impact: 2
residual_probability: 1
residual_impact: 2
strategy: mitigate
status: open
owner:
review: release
---
# R9: Globale Variable `SCAN_INTERVAL` wird im Konstruktor überschrieben

## Risikobeschreibung

Wenn mehrere Entries mit verschiedenen Intervallen eingerichtet sind, dann überschreibt jeder Konstruktor die globale Variable, was dazu führt, dass der zuletzt gesetzte Wert als Standard gilt.

## Befund im Detail

**Befund.** `SCAN_INTERVAL` ist eine globale Variable, die im Konstruktor überschrieben wird.

**Wirkung.** Bei mehreren Entries gilt der zuletzt gesetzte Wert für den Standard. Der Koordinator nutzt das Intervall allerdings über `update_interval=SCAN_INTERVAL` im Aufruf direkt danach, daher meist harmlos.

## Bewertung

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Bewertung | 2 | 2 | 4 | niedrig |
| Restrisiko nach der Gegenmaßnahme | 1 | 2 | 2 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.
<!-- /risk:assessment -->

## Gegenmaßnahme

Das Intervall je Koordinator halten statt global. Vorschlag, nicht umgesetzt.

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
