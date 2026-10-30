# Architekturentscheidungen (ADR)

Jede Entscheidung steht in einer eigenen Datei, nummeriert fortlaufend. Die Einträge ADR-0001 bis ADR-0009 sind aus Code und Kommentaren **rekonstruiert**, weil der Autor keine Entscheidungsprotokolle führt. ADR-0010 und ADR-0011 stammen aus dem Verlauf der Zusammenarbeit im Oktober 2026. Englische Fassungen liegen in [`en/`](en/README.md).

| ADR | Titel | Status |
|---|---|---|
| [ADR-0001](0001-prefer-websocket-polling-as-fallback.md) | WebSocket bevorzugen, Polling als Rückfall | Akzeptiert (rekonstruiert, Datum unbekannt) |
| [ADR-0002](0002-operating-mode-follows-from-the-password.md) | Betriebsart ergibt sich aus dem Passwort | Akzeptiert (rekonstruiert, Datum unbekannt) |
| [ADR-0003](0003-bridge-as-a-sub-library-in-the-same-folder.md) | Bridge als Teilbibliothek im selben Ordner | Akzeptiert (rekonstruiert, Datum unbekannt) |
| [ADR-0004](0004-declarative-entity-descriptions.md) | Deklarative Entity-Beschreibungen | Akzeptiert (rekonstruiert, Datum unbekannt) |
| [ADR-0005](0005-own-chainmap-data-store-instead-of-a-type-model.md) | Eigene ChainMap-Datenhaltung statt Typmodell | Akzeptiert (rekonstruiert, Datum unbekannt) |
| [ADR-0006](0006-hibernation-in-polling.md) | Hibernation im Polling | Akzeptiert (rekonstruiert, Datum unbekannt) |
| [ADR-0007](0007-pv-data-through-an-ha-automation-instead-of-extra-hardware.md) | PV-Daten über eine HA-Automation statt Zusatzhardware | Akzeptiert (rekonstruiert, Datum unbekannt) |
| [ADR-0008](0008-restart-by-config-reload-on-persistent-errors.md) | Neustart per Konfigurations-Reload bei dauerhaften Fehlern | Akzeptiert (rekonstruiert, Datum unbekannt) |
| [ADR-0009](0009-no-automated-tests-in-the-repository.md) | Keine automatisierten Tests im Repository | Ersetzt durch ADR-0011 |
| [ADR-0010](0010-service-calls-without-configid-only-with-exactly-one-charger.md) | Dienstaufrufe ohne configid nur bei genau einem Charger | Akzeptiert (2026-10-29, Commit `4702213`) |
| [ADR-0011](0011-regression-tests-in-the-repository.md) | Regressionstests im Repository | Akzeptiert (2026-10-29, PR #178 und #179) |

## Eine neue Entscheidung festhalten

1. Nächste freie Nummer wählen, Datei `NNNN-kurzer-titel.md` anlegen, Aufbau wie in den vorhandenen Dateien: Status, Kontext und Begründung, Entscheidung, Konsequenzen, Herkunft.
2. Wird eine Entscheidung abgelöst, den alten Eintrag nicht löschen, sondern den Status auf „Ersetzt durch ADR-NNNN“ setzen.
3. Die Tabelle oben und das Kapitel 9 der [arc42-Dokumentation](../architecture/arc42-ha-goecharger-api2.md) ergänzen. Die englische Fassung (`en/`) im selben Schritt pflegen.
