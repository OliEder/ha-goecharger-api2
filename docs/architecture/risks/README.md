# Risikoregister: `ha-goecharger-api2`

Alle bekannten Risiken und technischen Schulden der Integration, **ein Dokument je Risiko** (wie die Architekturentscheidungen in [`../adr/`](../adr/README.md)). Das Register gehört zur [arc42-Dokumentation](../arc42-ha-goecharger-api2.md) (Kapitel 11). Deutsch ist die Quelle, die englische Fassung liegt in [`en/`](en/README.md); beide werden gemeinsam gepflegt.

| | |
|---|---|
| **Stand** | 2026-10-30, `main` bei `e6ee0c3` |
| **Herkunft** | Ein mit KI-Unterstützung (Claude Code) erstellter und von einem Menschen geprüfter Abgleich von Code, Doku und Tests. Nichts davon wurde am echten Charger geprüft, außer wo ausdrücklich vermerkt. |
| **Datum erfasst** | Der Tag, an dem das Risiko in diese Dokumentation kam. Bei R15 bis R23 wurde der genaue Tag nicht nachverfolgt; 2026-10-29 ist der Tag, an dem sie ins Register kamen. |

## Wie die Risiken bewertet sind

Jedes Dokument formuliert das Risiko als „Wenn [Ursache], dann [Ereignis], was zu [Auswirkung] führt“, nennt Eintrittswahrscheinlichkeit W und Schadensauswirkung A (1 bis 5), den Score W × A, die Strategie (mindern, akzeptieren, vermeiden, verlagern), eine Gegenmaßnahme und das Restrisiko. **W, A und Strategie sind Einschätzungen, keine Messwerte.** Ein Risk Owner ist nicht benannt; der Maintainer sollte einen festlegen. Prüfung: bei jedem neuen Release.

Score-Stufen: 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.

## Offene Risiken (Heatmap)

| W \ A | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **5** | R7 |   |   |   |   |
| **4** |   |   |   |   |   |
| **3** | R10 | R6, R12, R17, R26, R29 | R11, R14, R20, R23, R30 | R16 |   |
| **2** | R18 | R9 | R8, R21 | R19 |   |
| **1** | R22 |   |   |   |   |

(Nur offene Risiken und Hinweise. Geschlossene stehen in der Tabelle unten.)

## Alle Risiken

| ID | Titel | Kategorie | W | A | Score | Strategie | Status |
|---|---|---|---|---|---|---|---|
| [R1](R001-stop-charging-locks-the-charger-after-a-write-error.md) | stop_charging sperrt den Charger nach einem Schreibfehler | Technologie / Architektur | 3 | 4 | 12 (mittel) | Mindern | Geschlossen (behoben) |
| [R2](R002-multi-charger-registry-incomplete.md) | Multi-Charger-Register unvollständig | Technologie / Architektur | 3 | 3 | 9 (mittel) | Mindern | Geschlossen (behoben) |
| [R3](R003-active-charger-counter-with-controller-entries.md) | Zähler der aktiven Charger bei Controller-Entries | Technologie / Architektur | 2 | 3 | 6 (mittel) | Mindern | Geschlossen (behoben) |
| [R4](R004-error-handling-for-multiple-writes-calls-the-wrong-sign.md) | Fehlerbehandlung beim Mehrfachschreiben ruft falsche Signatur auf | Technologie / Architektur | 2 | 2 | 4 (niedrig) | Mindern | Geschlossen (behoben) |
| [R5](R005-pgrid-without-a-finiteness-check.md) | `pgrid` ohne Endlichkeitsprüfung | Technologie / Architektur | 1 | 3 | 3 (niedrig) | Mindern | Geschlossen (behoben) |
| [R6](R006-no-unique-id-in-the-config-flow.md) | Keine `unique_id` im Config-Flow | Technologie / Architektur | 3 | 2 | 6 (mittel) | Mindern | Offen |
| [R7](R007-readme-and-code-state-different-read-intervals-for-the.md) | README und Code nennen verschiedene Leseintervalle der Konfiguration | Dokumentation | 5 | 1 | 5 (niedrig) | Mindern | Offen |
| [R8](R008-credentials-are-stored-in-plain-text-in-the-config-entr.md) | Zugangsdaten liegen im Klartext im Config-Entry | Security & Datenschutz | 2 | 3 | 6 (mittel) | Akzeptieren | Akzeptiert (Hinweis) |
| [R9](R009-global-variable-scan-interval-is-overwritten-in-the-con.md) | Globale Variable `SCAN_INTERVAL` wird im Konstruktor überschrieben | Wartbarkeit | 2 | 2 | 4 (niedrig) | Mindern | Offen |
| [R10](R010-check-and-write-to-16a-accesses-private-members.md) | `check_and_write_to_16a` greift auf Privates zu | Wartbarkeit | 3 | 1 | 3 (niedrig) | Mindern | Offen |
| [R11](R011-bcrypt-missing-in-the-manifest-minimum-home-assistant-v.md) | `bcrypt` fehlt im Manifest, Mindestversion von Home Assistant unklar | Integration / Drittanbieter | 3 | 3 | 9 (mittel) | Mindern | Offen |
| [R12](R012-customfriendlynameentity-overrides-a-private-ha-method.md) | `CustomFriendlyNameEntity` überschreibt eine private HA-Methode | Integration / Drittanbieter | 3 | 2 | 6 (mittel) | Mindern | Offen |
| [R13](R013-no-automated-tests-in-the-repository.md) | Keine automatisierten Tests im Repository | Qualität / Test | 4 | 3 | 12 (mittel) | Mindern | Geschlossen (überholt) |
| [R14](R014-entities-stay-available-on-partial-failure-and-show-old.md) | Entitäten bleiben bei Teilausfall `available` und zeigen alte Werte | Technologie / Architektur | 3 | 3 | 9 (mittel) | Mindern | Offen |
| [R15](R015-cloud-documentation-names-http-202-for-api-set.md) | Cloud-Dokumentation nennt für `/api/set` HTTP 202 | Integration / Drittanbieter | 2 | 3 | 6 (mittel) | Akzeptieren | Geschlossen (geklärt, kein Fehler) |
| [R16](R016-websocket-interface-is-not-officially-documented.md) | WebSocket-Schnittstelle ist nicht offiziell dokumentiert | Integration / Drittanbieter | 3 | 4 | 12 (mittel) | Mindern | Offen |
| [R17](R017-cloud-data-can-be-up-to-30-seconds-old.md) | Cloud-Daten können bis zu 30 Sekunden alt sein | Integration / Drittanbieter | 3 | 2 | 6 (mittel) | Mindern | Offen |
| [R18](R018-negative-ppv-standby-cannot-be-set.md) | `ppv` negativ (Standby) lässt sich nicht setzen | Integration / Drittanbieter | 2 | 1 | 2 (niedrig) | Akzeptieren | Offen |
| [R19](R019-cloud-token-is-readable-via-the-key-cak-according-to-th.md) | Cloud-Token ist laut Doku über den Schlüssel `cak` lesbar | Security & Datenschutz | 2 | 4 | 8 (mittel) | Mindern | Offen |
| [R20](R020-old-values-stay-after-a-failed-read.md) | Nach fehlgeschlagenem Lesen bleiben alte Werte stehen | Technologie / Architektur | 3 | 3 | 9 (mittel) | Mindern | Offen |
| [R21](R021-migration-from-2-0-to-2-1-deletes-all-devices.md) | Migration von 2.0 auf 2.1 löscht alle Geräte | Technologie / Architektur | 2 | 3 | 6 (mittel) | Mindern | Offen |
| [R22](R022-version-1-entries-leave-old-devices-in-the-registry.md) | Version-1-Entries lassen alte Geräte in der Registry | Wartbarkeit | 1 | 1 | 1 (niedrig) | Akzeptieren | Offen |
| [R23](R023-blueprint-in-main-has-no-zero-value-branch-for-invalid.md) | Blueprint in `main` hat bei ungültigen Messwerten keinen Nullwert-Zweig | Integration / Drittanbieter | 3 | 3 | 9 (mittel) | Mindern | Offen |
| [R24](R024-error-text-of-the-charger-counts-as-success.md) | Fehlertext des Chargers gilt als Erfolg | Technologie / Architektur | 2 | 3 | 6 (mittel) | Mindern | Geschlossen (behoben) |
| [R25](R025-specific-start-error-message-is-covered-up.md) | Konkrete Startfehlermeldung wird überdeckt | Technologie / Architektur | 3 | 1 | 3 (niedrig) | Mindern | Geschlossen (behoben) |
| [R26](R026-rejected-value-stays-in-the-display.md) | Abgelehnter Wert bleibt in der Anzeige stehen | Technologie / Architektur | 3 | 2 | 6 (mittel) | Mindern | Offen |
| [R27](R027-false-error-after-a-successful-multiple-write.md) | Falscher `ERROR` nach erfolgreichem Mehrfachschreiben | Technologie / Architektur | 5 | 1 | 5 (niedrig) | Mindern | Geschlossen (behoben) |
| [R29](R029-without-cablecurrentlimit-there-is-no-limit-to-16-a-any.md) | Ohne `cableCurrentLimit` wird nicht mehr auf 16 A begrenzt | Integration / Drittanbieter | 3 | 2 | 6 (mittel) | Mindern | Offen |
| [R30](R030-max-ampere-is-reset-at-every-restart.md) | Max Ampere wird bei jedem Neustart zurückgesetzt | Technologie / Architektur | 3 | 3 | 9 (mittel) | Mindern | Offen |

## Anmerkungen

Die Nummer R28 wurde bewusst ausgelassen; die Nummerierung folgt der Reihenfolge der Funde.

Der Nachtrag zu R2 steht in [R2](R002-multi-charger-registry-incomplete.md).

## Offene Annahmen (nicht geprüft)

- Verhalten des Chargers nach einem Neustart mit gesetztem `frc=1`.
- Ob der Charger den PV-Datenschlüssel `ids` per WebSocket genauso annimmt wie per HTTP.
- Tatsächliche Mindestversion von Home Assistant.

## Ein neues Risiko festhalten

1. Nächste freie Nummer wählen, `RNNN-kurzer-titel.md` anlegen, Aufbau wie in den vorhandenen Dateien (Beschreibung, Befund, Bewertung, Gegenmaßnahme, Status, Beleg).
2. In die Tabelle und die Heatmap oben eintragen und die englische Fassung (`en/`) im selben Schritt pflegen.
3. Wird ein Risiko behoben, die Datei nicht löschen: Status auf „Geschlossen“ setzen und die Änderung nennen, die es behoben hat.
