# SPUR Telemetry Profile

**Publisher-facing requirements for the SPUR Telemetry standard.**

This repository is the **profile**. It names a single accreditation tier - Compliant - and the requirements an implementer must meet to be assessed at it: conformance to the standard, event-level delivery, real-time delivery, and a publisher-designated endpoint. Attribution consumers - parties that receive telemetry and redistribute per-publisher views - meet a parallel requirement set. The profile makes no requirement about query intent or topic classification.

The **standard** - the telemetry wire format itself - lives in a separate repository: [SPUR-Coalition/telemetry](https://github.com/SPUR-Coalition/telemetry). This profile references the standard by version and does not restate it.

## Why two repositories

The standard and the profile have different owners in the long run. The wire format is intended to move to a neutral standards body; the accreditation programme and conformance mark stay with the SPUR Coalition. Keeping them in separate repositories means the standard can transfer without disturbing the profile - the profile simply updates its version reference. See the standard's [GOVERNANCE.md](https://github.com/SPUR-Coalition/telemetry/blob/main/GOVERNANCE.md).

## What's in this repo

- [PROFILE.md](./PROFILE.md) - the profile: requirements, conformance assessment, conformance mark
- [accreditation/](./accreditation/) - example fixtures and the assessment runner
- [LICENSE](./LICENSE) - Mozilla Public License 2.0

## Compliant at a glance

| Requirement | Means |
|-------------|-------|
| Conformance to the standard | Conforming emitter at Retrieval, Grounding, or Attribution level |
| Event-level delivery | Discrete events per fetch / grounding / citation / display / engagement - no aggregation |
| Real-time delivery | Events dispatched as they occur; alternative cadence by per-publisher negotiation |
| Publisher-designated endpoint | Telemetry routed to a destination the publisher chooses |

Attribution consumers meet a parallel set (PROFILE.md section 5.5): standard consumer conformance, publisher resolution and isolation, and onward delivery to a publisher-designated endpoint.

See [PROFILE.md](./PROFILE.md) for the full definitions.

## Status

Preview (v0.1). Constrains SPUR Telemetry v0.1. Requirements may change before 1.0.
