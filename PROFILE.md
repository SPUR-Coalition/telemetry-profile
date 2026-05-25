# SPUR Telemetry Profile

Publisher accreditation tiers for the SPUR Telemetry standard.

**Version:** 0.1
**Status:** Preview
**Last updated:** 2026-05-25
**Constrains:** SPUR Telemetry Specification, version 0.1

## Contents

1. [Scope](#1-scope)
2. [Normative references](#2-normative-references)
3. [Terms and definitions](#3-terms-and-definitions)
4. [Relationship to the SPUR Telemetry standard](#4-relationship-to-the-spur-telemetry-standard)
5. [Accreditation tiers](#5-accreditation-tiers)
6. [Privacy floor](#6-privacy-floor)
7. [Conformance assessment](#7-conformance-assessment)
8. [The SPUR conformance mark](#8-the-spur-conformance-mark)
9. [Versioning](#9-versioning)

[Annex A](#annex-a--tier-summary) (informative) — Tier summary

## Introduction

The SPUR Telemetry standard defines a wire format for reporting how AI agents use content: which content was retrieved, whether it was grounded, cited, displayed, and engaged with. The standard is permissive by design. It defines what a telemetry event may contain and what a conforming emitter must produce at each conformance level, but it does not say which level a given implementer should reach, or what an implementer commits to beyond producing well-formed events.

This profile is that layer. It defines three accreditation tiers for implementers that report content telemetry to SPUR member publishers, the privacy floor that applies at each tier, and the behavioural commitments that come with each tier. An implementer is assessed against a tier and, if it qualifies, may display the corresponding SPUR conformance mark.

The standard and this profile are maintained separately. The standard defines the format; this profile defines the publisher-facing requirements layered on it. This profile adds requirements; it never modifies the wire format.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

## 1. Scope

This document specifies:

- three accreditation tiers — Compliant, Preferred, and Strategic partner
- the privacy floor that applies to conversation telemetry at each tier
- the behavioural commitments required at each tier
- how an implementer is assessed against a tier
- the conditions for displaying the SPUR conformance mark

This document does not specify:

- the telemetry wire format — event types, schema, conformance levels, transport (see the SPUR Telemetry Specification, the normative reference in section 2)
- attribution algorithms or counting models
- content access, licensing, or pricing terms
- privacy policies or data protection requirements

## 2. Normative references

| Reference | Description |
|-----------|-------------|
| SPUR Telemetry Specification, version 0.1 | The telemetry wire format this profile constrains. <https://github.com/SPUR-Coalition/telemetry> |
| RFC 2119 | Key words for use in RFCs to indicate requirement levels |
| RFC 8174 | Ambiguity of uppercase vs lowercase in RFC 2119 key words |

This profile constrains a fixed version of the SPUR Telemetry Specification. Where this document refers to "the standard", it means version 0.1 as cited above. Adoption of a later standard version is a deliberate revision of this profile (section 9).

## 3. Terms and definitions

The terms defined in the SPUR Telemetry Specification section 3 apply. In addition, for the purposes of this document:

### 3.1

**profile**

document that layers community-specific requirements on a standard: which conformance level is required, what privacy floor applies, and what behavioural commitments accompany conformance

### 3.2

**accreditation tier**

named level of conformance to this profile — Compliant, Preferred, or Strategic partner — combining a technical baseline, a privacy floor, and behavioural commitments

### 3.3

**privacy floor**

least-disclosure privacy level at which conversation telemetry may be reported to meet a tier (section 6)

### 3.4

**accredited implementer**

emitter or attribution consumer assessed as meeting a tier of this profile

### 3.5

**conformance mark**

visual mark a SPUR-accredited implementer may display to indicate its tier (section 8)

## 4. Relationship to the SPUR Telemetry standard

The standard defines the mechanism. This profile selects from it.

The standard defines three **conformance levels** — Retrieval, Grounding, and Attribution (standard, section 5.7) — and a **privacy mechanism**: the `privacy_level` field, the four levels `full`, `summary`, `intent`, and `minimal`, and the fields each level permits on a conversation turn (standard, section 5.5). The standard makes no conformance level and no privacy level mandatory for any relationship. An emitter producing well-formed Retrieval-level events at `minimal` privacy is fully conforming to the standard.

This profile builds on those mechanisms without changing them:

- each **accreditation tier** requires a specific **conformance level** from the standard;
- each tier sets a **privacy floor** — a point on the standard's privacy-level scale;
- each tier adds **behavioural commitments** that the standard does not address.

This profile adds requirements. It does not modify, reinterpret, or extend the wire format. An implementer that meets any tier of this profile is, by construction, conforming to the standard. An implementer can conform to the standard without engaging with this profile at all.

The dependency runs one way — profile to standard, never the reverse. The standard can therefore be transferred to another steward without disturbing this profile: the profile updates its section 2 reference to the standard's new location and version, and the tier definitions are unaffected.

## 5. Accreditation tiers

This profile defines three tiers. They are cumulative: each tier includes every requirement of the tier below it.

A tier has three components:

- a **technical baseline** — a conformance level from the standard, verified against the standard's reference tests;
- a **privacy floor** — see section 6;
- **behavioural commitments** — undertakings about how the implementer operates, beyond the events it emits.

### 5.1 Compliant

**Technical baseline.** The implementer is a conforming **Retrieval** emitter (standard, section 5.7.1): it reports `content_retrieved` events with `source_role` set, and at least one of `content_url` or `content_id` on every event. Verified against the standard's reference tests.

**Privacy floor.** None. Retrieval events carry no conversation turn, so no `privacy_level` applies (section 6).

**Behavioural commitments.**

- The implementer's reporting endpoint MUST allow a publisher to route that publisher's own events to a destination of the publisher's choice. Telemetry about a publisher's content is not locked to a single consumer.

A CDN reporting fetch events from edge servers, with no further commitments, meets Compliant. So does an AI platform that reports grounding events but reveals nothing about the user's question: it conforms to the standard, but sits below the Preferred privacy floor and is therefore assessed at Compliant.

### 5.2 Preferred

**Technical baseline.** The implementer is a conforming **Grounding** emitter (standard, section 5.7.2): in addition to the Retrieval requirements, it produces session documents and emits `content_grounded` and turn events.

**Privacy floor.** `intent`. Every conversation turn the implementer emits MUST carry a `privacy_level` of `intent`, `summary`, or `full`. Turns at `minimal` do not meet this tier (section 6).

**Behavioural commitments.**

- The implementer MUST publish reporting cadence and completeness figures — how often telemetry is delivered, and what proportion of eligible sessions or events it covers.
- The implementer MUST opt in to independent audit of those figures once an audit programme is available.
- Reporting endpoints MUST support aggregated reporting across multiple sources, so a publisher receiving telemetry from several implementers can consolidate it.
- A marketplace operating at this tier MUST support licensing and pricing tied to the telemetry it reports.

An AI platform that reports grounding at `intent` privacy, publishes completeness figures, and commits to audit meets Preferred.

### 5.3 Strategic partner

**Technical baseline.** The implementer is a conforming **Attribution** emitter (standard, section 5.7.3): in addition to the Grounding requirements, it emits `content_cited` events, and emits `content_displayed` and `content_engaged` events where applicable.

**Privacy floor.** `intent`, as for Preferred (section 6).

**Behavioural commitments.**

- The implementer MUST be an active participant in the SPUR telemetry working group.
- The implementer MUST publicly commit to interoperating with publisher-chosen reporting endpoints. Telemetry destinations are the publisher's choice, not the implementer's.

An AI platform that reports the full lifecycle through to engagement, publishes completeness figures, opts in to audit, participates in the working group, and commits publicly to endpoint interoperability meets Strategic partner.

## 6. Privacy floor

The standard defines four privacy levels for conversation telemetry, ordered here from least to most disclosure:

```
minimal  <  intent  <  summary  <  full
```

`minimal` shares only token counts and content URLs. `intent` adds the classified intent and topics of the user's question. `summary` adds a summarised query and response. `full` shares the verbatim query and response. The standard, section 5.5, defines exactly which fields each level permits.

The **privacy floor** is the least-disclosure level this profile accepts for a tier. It is a floor on *disclosure*, not a cap: it ensures the telemetry is informative enough to be useful for attribution. The standard's design ensures that telemetry at or above the floor still protects the user — `intent` reports what a question was about without reporting the question itself.

| Tier | Privacy floor | Meaning |
|------|---------------|---------|
| Compliant | None | Retrieval events carry no conversation turn |
| Preferred | `intent` | Every turn at `intent`, `summary`, or `full`; `minimal` turns do not qualify |
| Strategic partner | `intent` | As Preferred |

The floor applies to every conversation turn the implementer emits. A single turn below the floor places the implementer below the tier, assessed at the next tier down.

This profile sets the floor at `intent` and no higher. It does not require `summary` or `full`. Reporting the topic and intent of a question is enough to attribute content influence; the verbatim question is not needed for attribution and is not required by any tier.

## 7. Conformance assessment

An implementer is assessed against the highest tier whose requirements it meets in full. Assessment has three parts:

1. **Technical baseline** — verified against the standard's reference test suite for the relevant conformance level. An objective, repeatable check.
2. **Privacy floor** — verified by inspecting the `privacy_level` on emitted conversation turns. This is an application-layer check, since the standard's JSON Schema cannot express it (standard, section 5.7).
3. **Behavioural commitments** — verified by attestation, and by published evidence where the commitment is to publish something (cadence and completeness figures, working group participation, the public interoperability commitment).

The [`accreditation/`](./accreditation/) directory holds tier fixtures: example telemetry that does and does not meet each tier's technical baseline and privacy floor. Behavioural commitments cannot be fixture-tested and are assessed separately.

Assessment is self-attested in this preview version. An independent audit programme is anticipated; the Preferred and Strategic partner tiers require an implementer to opt in to it once available (section 5).

## 8. The SPUR conformance mark

A SPUR-accredited implementer may display the SPUR conformance mark for the tier at which it is assessed.

- The mark names the tier — Compliant, Preferred, or Strategic partner.
- The mark MUST NOT be displayed for a tier above the one at which the implementer is assessed.
- The mark refers to a specific version of this profile. An implementer reassessed against a later profile version updates the mark accordingly.
- The SPUR Coalition may withdraw the right to display the mark from an implementer that no longer meets the tier.

The conformance mark is a trademark of the SPUR Coalition. Permission to display it is granted through accreditation and is separate from the [Mozilla Public License 2.0](./LICENSE) that covers this document. The MPL does not grant any right to use the mark or other SPUR trademarks; that right is conveyed only through accreditation.

Mark artwork and detailed display rules are published separately by the SPUR Coalition.

## 9. Versioning

This profile is versioned independently of the standard it constrains.

Preview versions (0.x) may change tier definitions, privacy floors, and behavioural commitments as the accreditation programme develops. From 1.0 onward, a change that moves an implementer between tiers is a major version change.

This profile constrains a fixed version of the standard (section 2). When the SPUR Telemetry standard publishes a new version, the working group decides whether this profile adopts it. Adoption is a deliberate revision: the section 2 reference changes, and the change is published as a new profile version. The standard advancing does not change this profile until the profile is revised to follow it.

If stewardship of the standard transfers to another body, this profile updates its section 2 reference to the standard's new name and location. The tier definitions are unaffected — they reference conformance levels and privacy levels, which are properties of the format, not of its steward.

## Annex A — Tier summary

(informative)

| | Compliant | Preferred | Strategic partner |
|--|-----------|-----------|-------------------|
| Technical baseline | Retrieval conformance | Grounding conformance | Attribution conformance |
| Events | `content_retrieved` | + `content_grounded`, turn events | + `content_cited`, `content_displayed`, `content_engaged` |
| Privacy floor | None | `intent` | `intent` |
| Endpoint | Publisher-routable | + aggregated reporting | + public interoperability commitment |
| Reporting figures | — | Cadence + completeness published | As Preferred |
| Audit | — | Opt in when available | Opt in when available |
| Working group | — | — | Active participant |

Each tier includes every requirement of the tier to its left.
