# ADR-0005: Eigene ChainMap-Datenhaltung statt Typmodell

## Status

Akzeptiert (rekonstruiert, Datum unbekannt)

## Kontext und Begründung

Schnelle Anpassung an neue Schlüssel

## Entscheidung

Eigene `ChainMap`-Datenhaltung statt Typmodell

## Konsequenzen

Kein Schema; Fehler zeigen sich erst zur Laufzeit (`KeyError` werden abgefangen)

## Herkunft dieses Eintrags

Rekonstruiert aus Code und Kommentaren [Schluss]. Der Autor führt keine Entscheidungsprotokolle; die Begründung ist abgeleitet, nicht belegt.

Architektur: [arc42](../architecture/arc42-ha-goecharger-api2.md) | [Zurück zum Index](README.md)
