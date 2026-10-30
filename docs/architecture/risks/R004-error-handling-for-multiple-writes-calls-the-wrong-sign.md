# R4: Fehlerbehandlung beim Mehrfachschreiben ruft falsche Signatur auf

| Feld | Wert |
|---|---|
| ID | R4 |
| Datum erfasst | 2026-10-27 |
| Kategorie | Technologie / Architektur |
| Status | Geschlossen (behoben) |
| Risk Owner | nicht benannt (vom Maintainer festzulegen) |
| Nächste Prüfung | bei jedem neuen Release |

## Risikobeschreibung

Wenn die Verbindung während eines Mehrfachschreibens (Fahrzeugauswahl `ct`) abbricht, dann wird `_handle_client_connection_error` mit einem Argument statt zwei aufgerufen, was dazu führt, dass ein `TypeError` die saubere Fehlerbehandlung ersetzt.

## Befund im Detail

**Befund.** `async_write_multiple_keys`: `_handle_client_connection_error` wird mit einem Argument statt zwei aufgerufen (`__init__.py:674`).

**Wirkung.** `TypeError` statt sauberer Fehlerbehandlung bei Verbindungsabbruch während des Schreibens (betrifft die Fahrzeugauswahl `ct`).

## Bewertung

| | W | A | Risikoscore | |
|---|---|---|---|---|
| Bewertung | 2 | 2 | 4 | niedrig |
| Restrisiko nach der Gegenmaßnahme | 1 | 2 | 2 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.

## Gegenmaßnahme

Der Aufruf hat jetzt zwei Argumente (`03b0fc3`).

## Status und Verlauf

Geschlossen (behoben) – `03b0fc3`. Aufruf hat jetzt zwei Argumente.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Im Test nachgespielt. Noch in `main`.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
