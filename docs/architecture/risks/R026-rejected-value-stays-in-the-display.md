# R26: Abgelehnter Wert bleibt in der Anzeige stehen

| Feld | Wert |
|---|---|
| ID | R26 |
| Datum erfasst | 2026-10-29 |
| Kategorie | Technologie / Architektur |
| Status | Offen |
| Risk Owner | nicht benannt (vom Maintainer festzulegen) |
| Nächste Prüfung | bei jedem neuen Release |

## Risikobeschreibung

Wenn der Charger einen Schreibbefehl im WebSocket-Modus ablehnt, dann hat die Integration den gewünschten Wert schon in `coordinator.data` übernommen, was dazu führt, dass Home Assistant den abgelehnten Wert anzeigt, bis das Gerät den Schlüssel erneut meldet.

## Befund im Detail

**Befund.** Nach `03b0fc3` speichert das Schreiben im WebSocket-Modus den gewünschten Wert sofort in `coordinator.data`.

**Wirkung.** Lehnt der Charger ab (nur eine Warnung im Log), zeigt HA den abgelehnten Wert, bis das Gerät den Schlüssel erneut meldet.

## Bewertung

| | W | A | Risikoscore | |
|---|---|---|---|---|
| Bewertung | 3 | 2 | 6 | mittel |
| Restrisiko nach der Gegenmaßnahme | 1 | 2 | 2 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.

## Gegenmaßnahme

Den Wert erst nach der Bestätigung übernehmen oder bei Ablehnung zurücksetzen; `require_ack` gibt es seit PR #177, nutzt es aber nur für `tcl` und `stop_charging`. Vorschlag. Das heutige Verhalten ist im Test festgehalten.

## Status und Verlauf

Offen.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Aus Code abgeleitet, Verhalten im Test festgehalten.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
