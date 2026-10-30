# Quality documentation

Written with AI assistance (Claude Code) and reviewed by a human. Merged into this repository with PR #178.

- `arc42-ha-goecharger-api2.md`: architecture documentation (arc42, German) reconstructed from code, README and the official go-e API documentation. Statements are marked as code, documentation or inference. Chapter 11 lists risks and shows which of them have been fixed upstream.
- `testkonzept-ha-goecharger-api2.md`: test concept (scope, levels, markers, current state, gaps).
- `arc42-ha-goecharger-api2.en.md` and `testkonzept-ha-goecharger-api2.en.md`: English versions of both documents. The German files are the source; update both languages together.

Tests: `tests/integration/`. Measurement report: manually with `.github/workflows/test-report.yaml`. Tools: `tests/tools/`.
