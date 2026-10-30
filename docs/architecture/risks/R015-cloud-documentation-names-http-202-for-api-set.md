---
id: R15
date: 2026-10-29
category: INT
probability: 2
impact: 3
residual_probability: 1
residual_impact: 1
strategy: accept
status: settled
owner:
review: release
---
# R15: Cloud-Dokumentation nennt für `/api/set` HTTP 202

## Risikobeschreibung

Wenn die Cloud auf `/api/set` mit 202 statt 200 antwortete, dann würde der Code den Erfolg als Fehler werten, was dazu führen würde, dass Schreibbefehle im Cloud-Polling als fehlgeschlagen geloggt werden.

## Befund im Detail

**Befund.** Laut Cloud-Doku antwortet `/api/set` bei Erfolg mit **HTTP 202**. `_write_values_int` wertet nur `200` (und `500` mit Inhalt) aus, alles andere gilt als Fehler (`failed with http-status …`, Rückgabe `{}`).

**Wirkung.** Wenn die Cloud tatsächlich 202 sendet, würden Schreibbefehle im Cloud-Polling trotz Erfolg als Fehler geloggt, und `handle_write_result` meldet „could not write“. Im WebSocket-Betrieb ist der Pfad nicht betroffen.

## Bewertung

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Bewertung | 2 | 3 | 6 | mittel |
| Restrisiko nach der Gegenmaßnahme | 1 | 1 | 1 | niedrig |

Risikostrategie: **Akzeptieren**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.
<!-- /risk:assessment -->

## Gegenmaßnahme

Keine. Der Maintainer hat am 2026-10-29 im Issue #172 bestätigt, dass die echte Cloud 200 liefert und die Dokumentation falsch ist. Der Test erwartet 200.

## Status und Verlauf

<!-- risk:status -->
Geschlossen (geklärt, kein Fehler)
<!-- /risk:status -->

Maintainer, Issue #172.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Doku und Code gelesen. **Geklärt am 2026-10-29 durch den Maintainer (Issue #172): Die Cloud antwortet mit HTTP 200, die Doku ist falsch. Kein Fehler im Code.** Von uns nicht gegen die echte Cloud geprüft.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
