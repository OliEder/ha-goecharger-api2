# ADR-0001: WebSocket bevorzugen, Polling als Rückfall

## Status

Akzeptiert (rekonstruiert, Datum unbekannt)

## Kontext und Begründung

Effizienz; einige Geräte (Wattpilot) bieten kein HTTP-API [Doku]

## Entscheidung

WebSocket bevorzugen, Polling als Rückfall

## Konsequenzen

Zwei Datenpfade mit unterschiedlichem Schreibergebnis (`None` gegenüber Dictionary)

## Herkunft dieses Eintrags

Rekonstruiert aus Code und Kommentaren [Schluss]. Der Autor führt keine Entscheidungsprotokolle; die Begründung ist abgeleitet, nicht belegt.

Architektur: [arc42](../arc42-ha-goecharger-api2.md) | [Zurück zum Index](README.md)
