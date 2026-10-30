# R23: Blueprint in `main` hat bei ungültigen Messwerten keinen Nullwert-Zweig

| Feld | Wert |
|---|---|
| ID | R23 |
| Datum erfasst | 2026-10-29 |
| Kategorie | Integration / Drittanbieter |
| Status | Offen |
| Risk Owner | nicht benannt (vom Maintainer festzulegen) |
| Nächste Prüfung | bei jedem neuen Release |

## Risikobeschreibung

Wenn ein Sensor des PV-Blueprints tagsüber ausfällt, dann überspringt das Blueprint die Lieferung statt Nullwerte zu senden, was dazu führt, dass die gleitenden Mittelwerte der Wallbox stehen bleiben und ungewollt aus dem Netz geladen werden kann.

## Befund im Detail

**Befund.** Die in `main` gemergte Blueprint-Version (PR #171 plus #174, von marq24 manuell eingebaut) enthält **nicht** die Erweiterungen der ursprünglichen Fassung von PR #171: Bei ungültigen Messwerten wird die Tageslieferung **übersprungen** (kein Nullwert), bei falscher Zielauswahl `stop` mit `error: true` im 5-Sekunden-Takt, `mode: single` ohne `max_exceeded: silent`, kein Akku-Schalter, keine Karenzzeit. Das Verhalten steht im Blueprint-Text als bewusste Entscheidung („does not clear its previous averages“).

**Wirkung.** Fällt ein Sensor am Tag aus, bleiben die gleitenden Mittelwerte der Wallbox stehen. Dieses Risiko würde „Nullwerte senden“ vermeiden.

## Bewertung

| | W | A | Risikoscore | |
|---|---|---|---|---|
| Bewertung | 3 | 3 | 9 | mittel |
| Restrisiko nach der Gegenmaßnahme | 2 | 3 | 6 | mittel |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.

## Gegenmaßnahme

Das Verhalten ist im Blueprint als bewusste Entscheidung beschrieben. Eine Option „Nullwerte senden“ wäre die Gegenmaßnahme. Vorschlag.

## Status und Verlauf

Offen.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Quelltext gelesen.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
