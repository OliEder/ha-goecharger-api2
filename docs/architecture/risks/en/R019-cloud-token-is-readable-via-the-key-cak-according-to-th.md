# R19: Cloud token is readable via the key `cak` according to the documentation

| Field | Value |
|---|---|
| ID | R19 |
| Date recorded | 2026-10-29 |
| Category | Security & privacy |
| Status | Open |
| Risk owner | not named (to be set by the maintainer) |
| Next review | with every new release |

## Risk description

If the key `cak` is readable locally without login, then anyone on the network can read the cloud token, which means protecting the token in the config entry has only limited effect.

## Finding in detail

**Finding.** Officially the cloud token is readable via the key `cak` (so also via the local API, as far as the key is available there).

**Effect.** A measure of the integration to protect the token only in the config entry would then be only partly effective. I did not check whether `cak` is really readable locally without login.

## Assessment

| | W | A | Risk score | |
|---|---|---|---|---|
| Assessment | 2 | 4 | 8 | medium |
| Residual risk after the countermeasure | 2 | 3 | 6 | medium |

Risk strategy: **Mitigate**. Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.

## Countermeasure

Check whether `cak` is readable locally without login (read-only, on the device); depending on the result document it or advise the user to protect local access. Not checked.

## Status and history

Open.

## Evidence

*Evidence at the time of the finding (not today's state)*

Documentation only read.  

## Note on the assessment

W, A, strategy and residual risk are **assessments** by the author of this documentation (with AI assistance) [Schluss]. They are not measured and not agreed with the maintainer. The risk owner should confirm or change them.

Architecture: [arc42](../../arc42-ha-goecharger-api2.en.md) | [Back to the register](README.md)
