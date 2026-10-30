# R7: README und Code nennen verschiedene Leseintervalle der Konfiguration

| Feld | Wert |
|---|---|
| ID | R7 |
| Datum erfasst | 2026-10-27 |
| Kategorie | Dokumentation |
| Status | Offen |
| Risk Owner | nicht benannt (vom Maintainer festzulegen) |
| Nächste Prüfung | bei jedem neuen Release |

## Risikobeschreibung

Wenn Nutzer sich auf die Angabe „alle 24 Stunden“ im README verlassen, dann liest der Code die Konfiguration schon stündlich, was dazu führt, dass sie eine falsche Erwartung an die Last und die Aktualität haben.

## Befund im Detail

**Befund.** Dokumentation und Code weichen ab: README „Konfiguration alle 24 Stunden“, Code stündlich (`+ 3600`).

**Wirkung.** Falsche Erwartung bei Nutzern.

## Bewertung

| | W | A | Risikoscore | |
|---|---|---|---|---|
| Bewertung | 5 | 1 | 5 | niedrig |
| Restrisiko nach der Gegenmaßnahme | 1 | 1 | 1 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.

## Gegenmaßnahme

README oder Intervall anpassen. Vorschlag, nicht umgesetzt.

## Status und Verlauf

Offen.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Aus Code und README gelesen.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
