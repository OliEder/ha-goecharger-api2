---
id: R17
date: 2026-10-29
category: INT
probability: 3
impact: 2
residual_probability: 1
residual_impact: 2
strategy: mitigate
status: open
owner:
review: release
---
# R17: Cloud-Daten können bis zu 30 Sekunden alt sein

## Risikobeschreibung

Wenn die Integration `/api/status` der Cloud ohne den Parameter `age` abfragt, dann liefert die Cloud Daten bis 30 Sekunden Alter, was dazu führt, dass Werte im Cloud-Polling veraltet sind, ohne dass die Integration das erkennt.

## Befund im Detail

**Befund.** Cloud-`/api/status` liefert standardmäßig Daten bis 30 Sekunden Alter (`age=30`); die Integration setzt `age` nicht.

**Wirkung.** Im Cloud-Polling können Werte bis zu 30 Sekunden alt sein, ohne dass die Integration das erkennt.

## Bewertung

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Bewertung | 3 | 2 | 6 | mittel |
| Restrisiko nach der Gegenmaßnahme | 1 | 2 | 2 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.
<!-- /risk:assessment -->

## Gegenmaßnahme

`age` setzen oder den Header `last-modified` auswerten. Vorschlag, nicht umgesetzt.

## Status und Verlauf

<!-- risk:status -->
Offen
<!-- /risk:status -->

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Doku und Code gelesen (kein `age` in den Aufrufen).  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
