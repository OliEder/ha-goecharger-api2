# R6: Keine `unique_id` im Config-Flow

| Feld | Wert |
|---|---|
| ID | R6 |
| Datum erfasst | 2026-10-27 |
| Kategorie | Technologie / Architektur |
| Status | Offen |
| Risk Owner | nicht benannt (vom Maintainer festzulegen) |
| Nächste Prüfung | bei jedem neuen Release |

## Risikobeschreibung

Wenn ein Nutzer denselben Charger ein zweites Mal einrichtet, dann greift `_abort_if_unique_id_configured()` nicht, weil nie eine `unique_id` gesetzt wird, was dazu führt, dass doppelte Entries und doppelte Entitäten entstehen.

## Befund im Detail

**Befund.** `_abort_if_unique_id_configured()` wird aufgerufen, aber im Config-Flow wird nirgends eine `unique_id` gesetzt (`async_set_unique_id` kommt nicht vor).

**Wirkung.** Kein Schutz gegen doppelt angelegte Geräte.

## Bewertung

| | W | A | Risikoscore | |
|---|---|---|---|---|
| Bewertung | 3 | 2 | 6 | mittel |
| Restrisiko nach der Gegenmaßnahme | 1 | 2 | 2 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.

## Gegenmaßnahme

Im Config-Flow `async_set_unique_id` mit der Seriennummer aufrufen. Vorschlag, nicht umgesetzt.

## Status und Verlauf

Offen.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Aus Code gelesen (grep). Wirkung nicht vorgeführt.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
