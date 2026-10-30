---
id: R27
date: 2026-10-29
category: ARCH
probability: 5
impact: 1
residual_probability: 1
residual_impact: 1
strategy: mitigate
status: fixed
owner:
review: release
---
# R27: Falscher `ERROR` nach erfolgreichem Mehrfachschreiben

## Risikobeschreibung

Wenn der Nutzer im WebSocket-Modus den Fahrzeugtyp wechselt, dann liefert `write_multiple_values_to_keys` `{}` und `handle_write_result` überspringt nur `None`, was dazu führt, dass nach jeder erfolgreichen Auswahl ein falscher `ERROR` im Log steht.

## Befund im Detail

**Befund.** `write_multiple_values_to_keys` liefert im WebSocket-Modus `{}`; `handle_write_result` überspringt nur `None`.

**Wirkung.** Nach jeder erfolgreichen Fahrzeugauswahl steht ein falscher `ERROR` im Log („could not write multiple value“).

## Bewertung

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Bewertung | 5 | 1 | 5 | niedrig |
| Restrisiko nach der Gegenmaßnahme | 1 | 1 | 1 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.
<!-- /risk:assessment -->

## Gegenmaßnahme

`handle_write_result` überspringt im WebSocket-Modus auch ein leeres Ergebnis (`9e7d62a`).

## Status und Verlauf

<!-- risk:status -->
Geschlossen (behoben)
<!-- /risk:status -->

`9e7d62a`. Seit `9e7d62a` überspringt `handle_write_result` im WebSocket-Modus auch ein leeres Ergebnis.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Im Test gezeigt (`known_bug`).  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
