# R13: Keine automatisierten Tests im Repository

| Feld | Wert |
|---|---|
| ID | R13 |
| Datum erfasst | 2026-10-27 |
| Kategorie | Qualität / Test |
| Status | Geschlossen (überholt) |
| Risk Owner | nicht benannt (vom Maintainer festzulegen) |
| Nächste Prüfung | bei jedem neuen Release |

## Risikobeschreibung

Wenn Code geändert oder umgebaut wird, dann fehlt eine automatische Prüfung, was dazu führt, dass Regressionen erst bei Nutzern auffallen.

## Befund im Detail

**Befund.** Keine Tests im Repo (überholt: seit PR #178 liegen sie in `tests/integration`).

**Wirkung.** Regressionen werden erst von Nutzern gefunden.

## Bewertung

| | W | A | Risikoscore | |
|---|---|---|---|---|
| Bewertung | 4 | 3 | 12 | mittel |
| Restrisiko nach der Gegenmaßnahme | 2 | 3 | 6 | mittel |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.

## Gegenmaßnahme

Die Regressionstests liegen seit PR #178 im Repository und laufen seit PR #179 bei Push und Pull Request (ADR-0011). Sie prüfen mit Attrappen, nicht am Gerät; deshalb bleibt ein Restrisiko.

## Status und Verlauf

Geschlossen (überholt) – PR #178 und #179.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Repo-Inhalt.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
