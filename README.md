# SPUR Telemetry Profile

**Publisher-facing requirements for the SPUR Telemetry standard.**

This repository is the **profile**. It names a single accreditation tier - Compliant - and the requirements an implementer must meet to be assessed at it: conformance to the standard, event-level delivery, real-time delivery, and a publisher-designated endpoint. Attribution consumers - parties that receive telemetry and redistribute per-publisher views - meet a parallel requirement set. The profile makes no requirement about query intent or topic classification.

The **standard** - the telemetry wire format itself - lives in a separate repository: [SPUR-Coalition/telemetry](https://github.com/SPUR-Coalition/telemetry). This profile references the standard by version and does not restate it.

## Why two repositories

A standard and a profile are different kinds of document. The standard defines the wire format - what telemetry looks like on the wire - and stays free of any one community's requirements. The profile defines what an implementer must do to earn the SPUR conformance mark, and carries the accreditation programme. Separating them keeps the standard neutral and lets each evolve on its own cadence: the profile can change its requirements without touching the wire format, and other communities can write their own profiles against the same standard. The dependency runs one way - the profile references the standard by version; the standard never references the profile.

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
