---
id: R10
date: 2026-10-27
category: MAINT
probability: 3
impact: 1
residual_probability: 1
residual_impact: 1
strategy: mitigate
status: open
owner:
review: release
---
# R10: `check_and_write_to_16a` greift auf Privates zu

## Risikobeschreibung

Wenn die Bridge intern umgebaut wird, dann bricht `check_and_write_to_16a`, weil es als Funktion auf Modulebene die private Methode `bridge._read_filtered_data` aufruft, was dazu führt, dass die 16-A-Begrenzung stillschweigend ausfällt.

## Befund im Detail

**Befund.** `check_and_write_to_16a`: Funktion mit `@staticmethod` auf Modulebene, außerdem privater Zugriff auf `bridge._read_filtered_data`.

**Wirkung.** Wartbarkeit.

## Bewertung

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Bewertung | 3 | 1 | 3 | niedrig |
| Restrisiko nach der Gegenmaßnahme | 1 | 1 | 1 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.
<!-- /risk:assessment -->

## Gegenmaßnahme

Die Funktion in den Koordinator verlegen und eine öffentliche Bridge-Methode nutzen. Vorschlag, nicht umgesetzt.

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
