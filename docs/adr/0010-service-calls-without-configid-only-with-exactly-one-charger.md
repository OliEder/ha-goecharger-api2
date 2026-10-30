# ADR-0010: Dienstaufrufe ohne configid nur bei genau einem Charger

## Status

Akzeptiert (2026-10-29, Commit `4702213`)

## Kontext und Begründung

Vorher wurde der zuerst registrierte Charger genommen. Nach dem Neuladen eines Entries rückte dieser ans Ende der Liste, der Standard wechselte dann stillschweigend auf einen anderen Charger. Ein falscher Charger bei Schreibzugriffen (Strom, Stopp) wird vermieden [Schluss, aus Diff und Testfund].

## Entscheidung

Dienste (`set_pv_data`, `stop_charging`) ohne `configid`: nur bei genau einem registrierten Charger wird dieser verwendet, sonst `ServiceValidationError` (Commit `4702213`, 2026-10-29; Entscheidung des Maintainers im Code, im Issue #172 nicht begründet)

## Konsequenzen

**Verhaltensänderung:** Wer mehrere Charger hat und `configid` bisher wegließ (zum Beispiel ein Blueprint oder eine Automation), bekommt jetzt einen Fehler statt eines Zugriffs auf den ersten Charger. Mit einem Charger oder mit `configid` ändert sich nichts. `docs/PVSURPLUS.md` verlangt `configid` bei mehreren Chargern bereits; das Blueprint selbst enthält keine `configid` (per `grep` geprüft), ein Aufruf aus dem Blueprint mit mehreren Chargern scheitert deshalb jetzt, sofern der Nutzer sie nicht ergänzt. Am Gerät nicht nachgespielt.

## Alternativen

Nicht gewählt: festen Standard-Charger bestimmen oder die Reihenfolge stabil halten.

## Nachweis (Tests)

`test_without_configid_and_with_two_chargers_no_charger_is_guessed`, `test_with_an_empty_registry_no_charger_can_be_chosen`.

## Herkunft dieses Eintrags

Aus Commit, Diff und Tests abgeleitet [Schluss]; die Begründung hat der Maintainer nicht schriftlich gegeben.

Architektur: [arc42](../architecture/arc42-ha-goecharger-api2.md) | [Zurück zum Index](README.md)
