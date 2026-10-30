# R24: Fehlertext des Chargers gilt als Erfolg

| Feld | Wert |
|---|---|
| ID | R24 |
| Datum erfasst | 2026-10-29 |
| Kategorie | Technologie / Architektur |
| Status | Geschlossen (behoben) |
| Risk Owner | nicht benannt (vom Maintainer festzulegen) |
| Nächste Prüfung | bei jedem neuen Release |

## Risikobeschreibung

Wenn der Charger auf einen Schreibbefehl mit einem Fehlertext statt `true` antwortet, dann wertet `_write_values_int` die Antwort nur auf „wahr“, was dazu führt, dass Ablehnungen (auch bei `ids`) als Erfolg gemeldet werden.

## Befund im Detail

**Befund.** `_write_values_int` prüft die Antwort des Chargers auf den Schlüssel nur auf „wahr“. Laut `http-en.md` kann der Wert `true` oder ein **Fehlertext** sein. Ein Text gilt dem Code als Erfolg.

**Wirkung.** Ablehnungen des Chargers (auch bei `ids`) würden als Erfolg gemeldet.

## Bewertung

| | W | A | Risikoscore | |
|---|---|---|---|---|
| Bewertung | 2 | 3 | 6 | mittel |
| Restrisiko nach der Gegenmaßnahme | 1 | 3 | 3 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.

## Gegenmaßnahme

Der Test ist auf `main` bei `9e7d62a` grün; welche Änderung das bewirkt hat, wurde nicht nachverfolgt.

## Status und Verlauf

Geschlossen (behoben) – (Commit nicht nachverfolgt). Der Test `test_write_rejected_by_charger_returns_err` ist auf `9e7d62a` grün; wann genau die Antwort mit Fehlertext ausgewertet wird, habe ich nicht nachvollzogen.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Aus Code und Doku abgeleitet, im Test mit Attrappe gezeigt (`known_bug`). Am Gerät **nicht** geprüft.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
