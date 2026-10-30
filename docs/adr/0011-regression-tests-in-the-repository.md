# ADR-0011: Regressionstests im Repository

## Status

Akzeptiert (2026-10-29, PR #178 und #179)

## Kontext und Begründung

Der Maintainer hat die Tests in PR #178 und die angepassten Workflows in PR #179 übernommen. Davor gab es keine Tests im Repository (ADR-0009). Regressionen sollen vor einem Release auffallen, auch beim Umbau von Code [Schluss, aus dem Verlauf von Issue #172].

## Entscheidung

Die Regressionstests liegen im Repository (`tests/integration`) und laufen bei jedem Push auf `main` und bei jedem Pull Request (`.github/workflows/tests.yaml`). Offene Funde tragen die Marker `known_bug` oder `needs_decision` und sind nicht blockierend.

## Konsequenzen

Tests und Bericht müssen gepflegt werden; ein behobener Fund verlangt, den Marker von Hand zu entfernen. Die Tests prüfen mit Attrappen, nicht am Gerät (siehe Testkonzept).

## Herkunft dieses Eintrags

Aus Commit, Diff und Tests abgeleitet [Schluss]; die Begründung hat der Maintainer nicht schriftlich gegeben.

Architektur: [arc42](../architecture/arc42-ha-goecharger-api2.md) | [Zurück zum Index](README.md)
