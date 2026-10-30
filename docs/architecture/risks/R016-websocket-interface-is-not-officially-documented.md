# R16: WebSocket-Schnittstelle ist nicht offiziell dokumentiert

| Feld | Wert |
|---|---|
| ID | R16 |
| Datum erfasst | 2026-10-29 |
| Kategorie | Integration / Drittanbieter |
| Status | Offen |
| Risk Owner | nicht benannt (vom Maintainer festzulegen) |
| Nächste Prüfung | bei jedem neuen Release |

## Risikobeschreibung

Wenn go-e Firmware oder Cloud ändert, dann bricht die nachgebaute WebSocket-Anmeldung oder das Nachrichtenformat ohne Vorwarnung, was dazu führt, dass alle Nutzer im bevorzugten Betrieb (mit Passwort) keine Daten mehr erhalten.

## Befund im Detail

**Befund.** Der bevorzugte Datenpfad (WebSocket) ist nicht offiziell dokumentiert; Anmeldeverfahren und Nachrichten sind nachgebaut.

**Wirkung.** Eine Firmware- oder Cloud-Änderung von go-e kann ihn ohne Vorwarnung brechen. Das README erwähnt das schon für Firmware 60.2 und 60.4.

## Bewertung

| | W | A | Risikoscore | |
|---|---|---|---|---|
| Bewertung | 3 | 4 | 12 | mittel |
| Restrisiko nach der Gegenmaßnahme | 2 | 3 | 6 | mittel |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.

## Gegenmaßnahme

Firmware-Änderungen von go-e beobachten, die Anmeldung mit Tests absichern (die Attrappen erkennen eine Änderung von go-e nicht) und prüfen, ob bei Fehlschlag auf HTTP zurückgefallen werden kann. Vorschlag.

## Status und Verlauf

Offen.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Doku und README gelesen.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
