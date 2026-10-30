---
id: R1
date: 2026-10-27
category: ARCH
probability: 3
impact: 4
residual_probability: 1
residual_impact: 4
strategy: mitigate
status: fixed
owner:
review: release
---
# R1: stop_charging sperrt den Charger nach einem Schreibfehler

## Risikobeschreibung

Wenn der Dienst `stop_charging` im WebSocket-Modus aufgerufen wird und der erste Schreibzugriff (`frc=1`) oder der zweite (`frc=0`) fehlschlägt, dann bleibt der Charger gesperrt und das Flag `_stop_in_progress` gesetzt, was dazu führt, dass der Nutzer nicht mehr laden kann und weitere Stopp-Anfragen mit „already in progress“ abgewiesen werden.

## Befund im Detail

**Befund.** `stop_charging` im WebSocket-Modus: `write_value_to_key` liefert `None`, danach `Tag.FRC.key in resp` wirft `TypeError`; abgefangen wird nur `ValueError`. `frc=1` ist gesetzt, `frc=0` wird nie gesendet, `_stop_in_progress` bleibt `True`.

**Wirkung.** Charger bleibt gesperrt, bis jemand `frc` von Hand zurücksetzt.

## Bewertung

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Bewertung | 3 | 4 | 12 | mittel |
| Restrisiko nach der Gegenmaßnahme | 1 | 4 | 4 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.
<!-- /risk:assessment -->

## Gegenmaßnahme

`finally` setzt das Flag immer zurück, beide Schreibzugriffe verlangen eine Bestätigung (`require_ack`). Umgesetzt in `03b0fc3`, `9e7d62a` und `d876dfd`.

## Status und Verlauf

<!-- risk:status -->
Geschlossen (behoben)
<!-- /risk:status -->

`03b0fc3`, `9e7d62a`. Der `TypeError` im WebSocket-Modus ist weg (`write_value_to_key` liefert `{key: value}`), `_stop_in_progress` wird seit `9e7d62a` in einem `finally` zurückgesetzt. Beide Tests sind grün.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Im Test nachgespielt. **Nicht** an echtem Gerät geprüft. Noch in `main`.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
