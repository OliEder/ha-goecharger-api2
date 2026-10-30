---
id: R30
date: 2026-10-29
category: ARCH
probability: 3
impact: 3
residual_probability: 1
residual_impact: 3
strategy: mitigate
status: open
owner:
review: release
---
# R30: Max Ampere wird bei jedem Neustart zurückgesetzt

## Risikobeschreibung

Wenn Home Assistant oder die Integration neu startet, dann setzt die Integration laut Maintainer das Maximum der Stromstärke zurück, was dazu führt, dass ein eingestellter Wert verloren geht und die Grenze nicht mehr gilt, bis sie neu gesetzt wird.

## Befund im Detail

**Befund.** Laut Maintainer (Issue #176) setzt die Integration das Maximum der Stromstärke (Max Ampere) bei jedem Neustart zurück.

**Wirkung.** Ein zuvor eingestellter Wert geht verloren; die Grenze gilt dann nicht mehr, bis sie neu gesetzt wird.

## Bewertung

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Bewertung | 3 | 3 | 9 | mittel |
| Restrisiko nach der Gegenmaßnahme | 1 | 3 | 3 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.
<!-- /risk:assessment -->

## Gegenmaßnahme

Das Verhalten nachstellen und mit einem Test festhalten; dann die Ursache klären (16-A-Begrenzer oder Wertübernahme beim Start). Aussage des Maintainers, nicht von uns nachgespielt.

## Status und Verlauf

<!-- risk:status -->
Offen
<!-- /risk:status -->

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Aussage des Maintainers, **nicht** von uns nachgespielt und kein Test dazu. Ob das vom 16-A-Begrenzer (R29) oder von der Wertübernahme beim Start kommt, ist offen.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
