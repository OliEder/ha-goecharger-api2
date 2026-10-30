# R14: Entitäten bleiben bei Teilausfall `available` und zeigen alte Werte

| Feld | Wert |
|---|---|
| ID | R14 |
| Datum erfasst | 2026-10-27 |
| Kategorie | Technologie / Architektur |
| Status | Offen |
| Risk Owner | nicht benannt (vom Maintainer festzulegen) |
| Nächste Prüfung | bei jedem neuen Release |

## Risikobeschreibung

Wenn das Gerät teilweise ausfällt, dann bleiben die Daten stehen und die Entitäten `available`, solange der letzte Update-Erfolg anhält, was dazu führt, dass Nutzer und Automationen alte Werte für aktuell halten.

## Befund im Detail

**Befund.** Bei Teilausfall des Geräts: Daten bleiben stehen, Entitäten bleiben `available`, solange der letzte Update-Erfolg anhält.

**Wirkung.** Nutzer sieht alte Werte als aktuell.

## Bewertung

| | W | A | Risikoscore | |
|---|---|---|---|---|
| Bewertung | 3 | 3 | 9 | mittel |
| Restrisiko nach der Gegenmaßnahme | 2 | 3 | 6 | mittel |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.

## Gegenmaßnahme

Verfügbarkeit nach mehreren fehlgeschlagenen Lesezyklen oder bei WebSocket-Verlust auf „nicht verfügbar“ setzen. Vorschlag, nicht umgesetzt; es gibt keinen Test dazu.

## Status und Verlauf

Offen.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Aus Code gelesen (`available` = `last_update_success`). Wie sich ein WebSocket-Verlust auf die Verfügbarkeit auswirkt, habe ich nicht geprüft.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
