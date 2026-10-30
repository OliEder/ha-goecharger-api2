# ADR-0001: Prefer WebSocket, polling as fallback

## Status

Accepted (reconstructed, date unknown)

## Context and reasoning

Efficiency; some devices (Wattpilot) offer no HTTP API [Docs]

## Decision

Prefer WebSocket, polling as fallback

## Consequences

Two data paths with different write results (`None` versus dictionary)

## Origin of this entry

Reconstructed from code and comments [Inference]. The author keeps no decision records; the reasoning is inferred, not proven.

Architecture: [arc42](../arc42-ha-goecharger-api2.md) | [Back to the index](README.md)
