# R20: Nach fehlgeschlagenem Lesen bleiben alte Werte stehen

| Feld | Wert |
|---|---|
| ID | R20 |
| Datum erfasst | 2026-10-29 |
| Kategorie | Technologie / Architektur |
| Status | Offen |
| Risk Owner | nicht benannt (vom Maintainer festzulegen) |
| Nächste Prüfung | bei jedem neuen Release |

## Risikobeschreibung

Wenn ein Charger im Cloud-Betrieb offline geht, dann überschreiben `read_all_states`, `read_all_config` und `read_versions` den Zustand bei leerer Antwort nicht und der Fehlerzähler wird zurückgesetzt, was dazu führt, dass die Entitäten weiter die letzten Werte als gültig anzeigen.

## Befund im Detail

**Befund.** Seit `5328e74` überschreibt `read_all_states`, `read_all_config` und `read_versions` den gespeicherten Zustand nur noch, wenn die Antwort nicht leer ist (`if ret is not None and len(ret) > 0 …`). Davor wurde bei einem Fehler der Zustand geleert. `_read_filtered_data` gibt bei jedem Status außer 200/400 (zum Beispiel Cloud 403 oder 404 bei offline) `{}` zurück.

**Wirkung.** Der Koordinator behält die letzten Werte und meldet Erfolg. Ein offline gegangener Charger zeigt im Cloud-Betrieb die letzten Werte weiter an. Zusätzlich setzt `_async_update_data` den Fehlerzähler zurück, weil die `ChainMap` der alten Werte nicht leer ist.

## Bewertung

| | W | A | Risikoscore | |
|---|---|---|---|---|
| Bewertung | 3 | 3 | 9 | mittel |
| Restrisiko nach der Gegenmaßnahme | 2 | 3 | 6 | mittel |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.

## Gegenmaßnahme

Absicht mit dem Maintainer klären; ein Test auf das gewünschte Verhalten fehlt, bis das geklärt ist. Das heutige Verhalten ist als Charakterisierung festgehalten.

## Status und Verlauf

Offen.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Aus Diff und Code abgeleitet, **nicht getestet**. Ob die Anzeige wirklich „eingefroren“ bleibt, hängt davon ab, was HA mit unverändertem `last_update_success` macht.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
