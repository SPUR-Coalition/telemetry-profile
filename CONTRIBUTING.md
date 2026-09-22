# Contributing to the SPUR Content Telemetry Profile

> **Consultation draft; not adopted.** [Status and review](CONSULTATION.md).

## Accreditation consultation

Once the consultation opens, a short implementation example or PoC question is
enough to start. Maintainers can help identify the relevant requirement. Use
issues for design questions and pull-request comments for wording. Follow-up pull requests should target the
consultation branch until the programme is adopted.

Maintainers link PoC findings to decisions to retain, amend, defer or delete
requirements, update the affected fixtures and publish reasons before adoption.
Describe the implementation scenario; use synthetic
examples rather than credentials or confidential operational records. Public
assessment summaries and reproducible tests belong here. Outreach lists,
internal handoffs and provider-specific private evidence belong in programme
working records outside this repository.

## What belongs here

This repository contains the **profile** - the requirements for the Compliant tier and the SPUR conformance mark. It does not contain the telemetry wire format. Changes to event types, schema, or conformance levels belong in the [standard repository](https://github.com/SPUR-Coalition/telemetry).

| File | Purpose |
|------|---------|
| [PROFILE.md](./PROFILE.md) | The normative profile |
| [accreditation/](./accreditation/) | Role requirements, assessment procedures and example fixtures |
| [CONSULTATION.md](./CONSULTATION.md) | Draft status, review questions, participation and decisions needed before adoption |
| [bindings/](./bindings/) | How licensing layers (e.g. RSL) reference this profile |

## Proposing changes

Before submitting a PR:

1. Open an issue describing the change and its motivation (the **Profile feedback** template walks through the points below).
2. State which requirement is affected and whether the change moves implementers in or out of the Compliant tier.
3. If the change depends on a new version of the standard, reference the standard issue or version.
4. Update PROFILE.md and any affected fixtures in `accreditation/`.

## Adopting a new standard version

This profile constrains a fixed version of the Content Telemetry standard (PROFILE.md section 2). Adopting a later standard version is a revision: open an issue, update every site that pins the standard version - the PROFILE.md header and section 2 reference, the README status line, the accreditation fixtures' `schema_version`, and the standard checkout in the CI workflow - and publish a new profile version.

## Conventions

- British English.
- Sentence case for headings.
- RFC 2119 keywords (MUST, SHOULD, MAY) per PROFILE.md.

## Licensing

This profile is published under the [Creative Commons Attribution-ShareAlike 4.0 International licence](./LICENSE). By submitting a contribution you agree to license it under the same terms. The SPUR conformance mark is a trademark and is not licensed by CC BY-SA; it is granted only through accreditation (PROFILE.md section 7).
