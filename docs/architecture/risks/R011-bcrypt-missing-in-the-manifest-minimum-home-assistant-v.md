---
id: R11
date: 2026-10-27
category: INT
probability: 3
impact: 3
residual_probability: 1
residual_impact: 3
strategy: mitigate
status: open
owner:
review: release
---
# R11: `bcrypt` fehlt im Manifest, Mindestversion von Home Assistant unklar

## Risikobeschreibung

Wenn die Integration auf einem älteren Home Assistant oder ohne vorhandenes `bcrypt` installiert wird, dann fehlen Abhängigkeiten oder APIs, was dazu führt, dass die Installation oder der Start fehlschlägt.

## Befund im Detail

**Befund.** Fehlende Abhängigkeit im Manifest (`bcrypt`), Mindestversion von HA unklar (`hacs.json` 2023.8.0 gegenüber genutzten neueren APIs).

**Wirkung.** Installationsfehler auf älteren Systemen möglich.

## Bewertung

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Bewertung | 3 | 3 | 9 | mittel |
| Restrisiko nach der Gegenmaßnahme | 1 | 3 | 3 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.
<!-- /risk:assessment -->

## Gegenmaßnahme

`bcrypt` ins Manifest aufnehmen und die Mindestversion prüfen und in `hacs.json` anpassen. Vorschlag, nicht umgesetzt. Die Tests laufen nur mit der neuesten Version.

## Status und Verlauf

<!-- risk:status -->
Offen
<!-- /risk:status -->

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Aus Code und Manifest gelesen. Ob `bcrypt` über HA mitgeliefert wird, habe ich nicht geprüft.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
