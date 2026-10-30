---
id: R2
date: 2026-10-27
category: ARCH
probability: 3
impact: 3
residual_probability: 1
residual_impact: 3
strategy: mitigate
status: fixed
owner:
review: release
---
# R2: Multi-Charger-Register unvollständig

## Risikobeschreibung

Wenn mehrere go-eCharger in einer HA-Instanz eingerichtet sind und ein Entry neu geladen wird, dann fehlt der zweite Charger im Register oder der alte Koordinator bleibt eingetragen, was dazu führt, dass `configid` für den zweiten Charger nicht funktioniert oder über eine getrennte Bridge geschrieben wird.

## Befund im Detail

**Befund.** Multi-Charger: Das Register `_COORDINATOR_PER_CONFIGENTRYID_MAP` wird nur im Konstruktor von `GoeChargerApiV2Service` befüllt. Der Konstruktor läuft nur, wenn der Dienst noch nicht angemeldet ist, also nur für den ersten Charger. Ein zweiter Charger fehlt im Register, `configid=<zweiter>` führt zu `KeyError`. Wird der erste Entry entladen, bleibt dessen Koordinator im Register.

**Wirkung.** Der dokumentierte Multi-Charger-Betrieb über `configid` funktioniert für den zweiten Charger nicht.

**Nachtrag zu R2:**Das ist eine **Regression** aus Commit `5328e74` („housekeeping of tasks“). Vorher wurde pro Charger-Entry immer ein `GoeChargerApiV2Service` angelegt und trug seinen Koordinator ins Register ein, `configid` funktionierte also für jeden Charger. Seit `5328e74` entsteht der Dienst nur noch beim ersten Charger. Zusätzlich bleibt nach dem Neuladen eines Entries (zum Beispiel durch die automatische Neustart-Logik nach mehr als 5 Verbindungsfehlern) bei mehreren Chargern der **alte** Koordinator im Register; der Dienst schreibt dann über eine getrennte Bridge. Aus dem Diff und dem Code gelesen, nicht nachgespielt.

## Bewertung

<!-- risk:assessment -->
| | W | A | Score (W × A) | |
|---|---|---|---|---|
| Bewertung | 3 | 3 | 9 | mittel |
| Restrisiko nach der Gegenmaßnahme | 1 | 3 | 3 | niedrig |

Risikostrategie: **Mindern**. Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.
<!-- /risk:assessment -->

## Gegenmaßnahme

Das Register wird für jeden Charger gepflegt, ein Neuladen ersetzt den Koordinator (`03b0fc3`). Dass ohne `configid` kein Charger geraten wird, ist in ADR-0010 entschieden (`4702213`).

## Status und Verlauf

<!-- risk:status -->
Geschlossen (behoben)
<!-- /risk:status -->

`03b0fc3`, ADR-0010 (`4702213`). Register wird für jeden Charger gepflegt, Neuladen ersetzt den alten Koordinator. Der wechselnde Standard-Charger ist seit `4702213` über ADR-0010 entschieden (kein Standard bei mehreren Chargern).

## Beleg

*Beleg zum Zeitpunkt des Befundes (nicht der heutige Stand)*

Aus Code gelesen (`service.py:17,33,41`, `__init__.py:153`ff). **Nicht nachgespielt.**  

## Hinweis zur Bewertung

W, A, Strategie und Restrisiko sind **Einschätzungen** des Autors dieser Dokumentation (mit KI-Unterstützung) [Schluss]. Sie sind nicht gemessen und nicht mit dem Maintainer abgestimmt. Der Risk Owner soll sie bestätigen oder ändern.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Register](README.md)
