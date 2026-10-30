# R29: Ohne `cableCurrentLimit` wird nicht mehr auf 16 A begrenzt

| Feld | Wert |
|---|---|
| ID | R29 |
| Datum erfasst | 2026-10-29 |
| Kategorie | Integration / Drittanbieter |
| Status | Offen |
| Risk Owner | nicht benannt (vom Maintainer festzulegen) |
| Nächste Prüfung | bei jedem neuen Release |

## Risikobeschreibung

Wenn `cll` Inhalt, aber keinen `cableCurrentLimit` hat, dann setzt die Integration seit `98af3e0` keine 16-A-Grenze und prüft `adi` nicht, was dazu führt, dass Sliders höhere Werte erlauben, obwohl ein Adapter angeschlossen sein könnte.

## Befund im Detail

**Befund.** `98af3e0`: Fehlt `cableCurrentLimit` in `cll`, wird nicht mehr auf 16 A begrenzt und `adi` nicht mehr geprüft; Core-Geräte ohne den Schlüssel waren vorher vorsichtshalber begrenzt.

**Wirkung.** Sliders erlauben höhere Werte; der Charger begrenzt einen Adapter selbst. Die Annahme „nur Flex hat den Schlüssel“ ist nicht belegt.

## Bewertung

| | W | A | Risikoscore | |
|---|---|---|---|---|
| Bewertung | 3 | 2 | 6 | mittel |
| Restrisiko nach der Gegenmaßnahme | 2 | 2 | 4 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.

## Gegenmaßnahme

Lesend am Charger prüfen, welche Firmware `cableCurrentLimit` liefert, und die Annahme „nur Flex-Geräte“ belegen oder widerlegen; die Doku und die Changelogs sagen dazu nichts. Der Charger begrenzt einen Adapter selbst, das mindert die Auswirkung.

## Status und Verlauf

Offen.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Aus Diff gelesen, Verhalten im Test festgehalten.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
