---
id: R19
date: 2026-10-29
category: SEC
probability: 2
impact: 4
residual_probability: 2
residual_impact: 3
strategy: mitigate
status: open
owner:
review: release
---
# R19: Cloud-Token ist laut Doku über den Schlüssel `cak` lesbar

## Risikobeschreibung

Wenn der Schlüssel `cak` lokal ohne Anmeldung lesbar ist, dann kann jeder im Netz den Cloud-Token auslesen, was dazu führt, dass der Schutz des Tokens im Config-Entry nur begrenzt wirkt.

## Befund im Detail

**Befund.** Offiziell ist der Cloud-Token über den Schlüssel `cak` lesbar (also auch über die lokale API, soweit der Schlüssel dort verfügbar ist).

**Wirkung.** Eine Maßnahme der Integration, den Token nur im Config-Entry zu schützen, wäre dann nur begrenzt wirksam. Ob `cak` tatsächlich lokal ohne Anmeldung lesbar ist, habe ich nicht geprüft.

## Bewertung

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Bewertung | 2 | 4 | 8 | mittel |
| Restrisiko nach der Gegenmaßnahme | 2 | 3 | 6 | mittel |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.
<!-- /risk:assessment -->

## Gegenmaßnahme

Prüfen, ob `cak` lokal ohne Anmeldung lesbar ist (nur lesend, am Gerät); je nach Ergebnis dokumentieren oder dem Nutzer raten, den lokalen Zugriff zu schützen. Nicht geprüft.

## Status und Verlauf

<!-- risk:status -->
Offen
<!-- /risk:status -->

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Nur Doku gelesen.  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
