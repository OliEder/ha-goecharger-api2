# R18: `ppv` negativ (Standby) lässt sich nicht setzen

| Feld | Wert |
|---|---|
| ID | R18 |
| Datum erfasst | 2026-10-29 |
| Kategorie | Integration / Drittanbieter |
| Status | Offen |
| Risk Owner | nicht benannt (vom Maintainer festzulegen) |
| Nächste Prüfung | bei jedem neuen Release |

## Risikobeschreibung

Wenn ein Nutzer den Standby-Zustand der PV-Anlage über `set_pv_data` melden will, dann begrenzt die Oberfläche `ppv` auf Werte ab 0, was dazu führt, dass `pPv < 0` (Standby) nicht gesendet werden kann.

## Befund im Detail

**Befund.** Offiziell bedeutet `pPv < 0` „Standby“, der Dienst `set_pv_data` begrenzt `ppv` in der Oberfläche auf Werte ab 0.

**Wirkung.** Standby kann über die Oberfläche nicht gesetzt werden. Ob das gewollt ist, ist unklar.

## Bewertung

| | W | A | Risikoscore | |
|---|---|---|---|---|
| Bewertung | 2 | 1 | 2 | niedrig |
| Restrisiko nach der Gegenmaßnahme | 2 | 1 | 2 | niedrig |

Risikostrategie: **Akzeptieren**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.

## Gegenmaßnahme

Akzeptiert, bis der Maintainer klärt, ob das gewollt ist.

## Status und Verlauf

Offen.

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Doku und `services.yaml` gelesen.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
