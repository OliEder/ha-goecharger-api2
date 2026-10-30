# R8: Zugangsdaten liegen im Klartext im Config-Entry

| Feld | Wert |
|---|---|
| ID | R8 |
| Datum erfasst | 2026-10-27 |
| Kategorie | Security & Datenschutz |
| Status | Akzeptiert (Hinweis) |
| Risk Owner | nicht benannt (vom Maintainer festzulegen) |
| Nächste Prüfung | bei jedem neuen Release |

## Risikobeschreibung

Wenn jemand Zugriff auf die HA-Konfiguration oder ein Backup erhält, dann sind Passwort und Cloud-Token im Klartext lesbar, was dazu führt, dass er das Gerät oder das Cloud-Konto steuern kann.

## Befund im Detail

**Befund.** Zugangsdaten liegen im Klartext im Config-Entry (Eigenschaft von Home Assistant). Weitere Einzelheiten sind bewusst nicht aufgeführt.

**Wirkung.** –

## Bewertung

| | W | A | Risikoscore | |
|---|---|---|---|---|
| Bewertung | 2 | 3 | 6 | mittel |
| Restrisiko nach der Gegenmaßnahme | 2 | 3 | 6 | mittel |

Risikostrategie: **Akzeptieren**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.

## Gegenmaßnahme

Home Assistant stellt keinen Tresor bereit; das Risiko wird akzeptiert und liegt bei Home Assistant. Weitere Beobachtungen wurden dem Maintainer direkt mitgeteilt und stehen hier bewusst nicht.

## Status und Verlauf

Akzeptiert (Hinweis).

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

–  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
