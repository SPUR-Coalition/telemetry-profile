# SPUR Telemetry Profile

**Publisher accreditation tiers for the SPUR Telemetry standard.**

This repository is the **profile**. It defines three accreditation tiers — Compliant, Preferred, and Strategic partner — for implementers that report content telemetry to SPUR member publishers. Each tier combines a technical conformance level, a privacy floor, and a set of behavioural commitments, and carries a SPUR conformance mark.

The **standard** — the telemetry wire format itself — lives in a separate repository: [SPUR-Coalition/telemetry](https://github.com/SPUR-Coalition/telemetry). This profile references the standard by version and does not restate it.

## Why two repositories

The standard and the profile have different owners in the long run. The wire format is intended to move to a neutral standards body; the accreditation programme and conformance mark stay with the SPUR Coalition. Keeping them in separate repositories means the standard can transfer without disturbing the profile — the profile simply updates its version reference. See the standard's [GOVERNANCE.md](https://github.com/SPUR-Coalition/telemetry/blob/main/GOVERNANCE.md).

## What's in this repo

- [PROFILE.md](./PROFILE.md) - the profile: tiers, privacy floor, behavioural commitments, conformance mark
- [accreditation/](./accreditation/) - tier fixtures and assessment material
- [LICENSE](./LICENSE) - Mozilla Public License 2.0

## The tiers at a glance

| Tier | Technical baseline | Privacy floor | Adds |
|------|--------------------|---------------|------|
| Compliant | Retrieval conformance | None | Publisher-routable endpoints |
| Preferred | Grounding conformance | `intent` | Completeness figures, audit opt-in, aggregated reporting |
| Strategic partner | Attribution conformance | `intent` | Working group participation, public interoperability commitment |

See [PROFILE.md](./PROFILE.md) for the full definitions.

## Status

Preview (v0.1). Constrains SPUR Telemetry v0.1. Tier definitions may change before 1.0.
