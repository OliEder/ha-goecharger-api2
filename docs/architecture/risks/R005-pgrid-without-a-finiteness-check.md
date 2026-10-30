# R5: `pgrid` ohne Endlichkeitsprüfung

| Feld | Wert |
|---|---|
| ID | R5 |
| Datum erfasst | 2026-10-27 |
| Kategorie | Technologie / Architektur |
| Status | Geschlossen (behoben) |
| Risk Owner | nicht benannt (vom Maintainer festzulegen) |
| Nächste Prüfung | bei jedem neuen Release |

## Risikobeschreibung

Wenn `set_pv_data` mit `NaN` oder `inf` als `pgrid` aufgerufen wird, dann wird der Wert ungeprüft gesendet, was dazu führt, dass ungültiges JSON zum Charger geht.

## Befund im Detail

**Befund.** `set_pv_data` prüft `pgrid` nur mit `isinstance(Number)` (`service.py:59`), `ppv` und `pakku` jedoch auf Endlichkeit.

**Wirkung.** `NaN` oder `inf` als `pgrid` kann als ungültiges JSON zum Charger gehen.

## Bewertung

| | W | A | Risikoscore | |
|---|---|---|---|---|
| Bewertung | 1 | 3 | 3 | niedrig |
| Restrisiko nach der Gegenmaßnahme | 1 | 1 | 1 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.

## Gegenmaßnahme

`pgrid` wird wie `ppv` und `pakku` auf Endlichkeit geprüft (`eb5da46`). Das Blueprint prüft ohnehin.

## Status und Verlauf

Geschlossen (behoben) – `eb5da46`. Seit `eb5da46` prüft `set_pv_data` auch `pgrid` auf Endlichkeit.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Aus Code gelesen. Geringe Praxisrelevanz, da das Blueprint prüft.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
