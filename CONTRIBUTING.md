# Contributing to the SPUR Telemetry Profile

## What belongs here

This repository contains the **profile** - the requirements for the Compliant tier and the SPUR conformance mark. It does not contain the telemetry wire format. Changes to event types, schema, or conformance levels belong in the [standard repository](https://github.com/SPUR-Coalition/telemetry).

| File | Purpose |
|------|---------|
| [PROFILE.md](./PROFILE.md) | The normative profile |
| [accreditation/](./accreditation/) | Example fixtures and assessment material |

## Proposing changes

The profile's requirements affect every accredited implementer. Before submitting a PR:

1. Open an issue describing the change and its motivation.
2. State which requirement is affected and whether the change moves implementers in or out of the Compliant tier.
3. If the change depends on a new version of the standard, reference the standard issue or version.
4. Update PROFILE.md and any affected fixtures in `accreditation/`.

## Adopting a new standard version

This profile constrains a fixed version of the SPUR Telemetry standard (PROFILE.md section 2). Adopting a later standard version is a deliberate revision: open an issue, update the section 2 reference, and publish a new profile version.

## Conventions

- British English.
- Sentence case for headings.
- RFC 2119 keywords (MUST, SHOULD, MAY) per PROFILE.md.
