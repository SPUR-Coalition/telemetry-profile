# SPUR Telemetry Profile

Publisher-facing requirements for the SPUR Telemetry standard.

**Version:** 0.1
**Status:** Preview
**Last updated:** 2026-05-27
**Constrains:** SPUR Telemetry Specification, version 0.1

## Contents

1. [Scope](#1-scope)
2. [Normative references](#2-normative-references)
3. [Terms and definitions](#3-terms-and-definitions)
4. [Relationship to the SPUR Telemetry standard](#4-relationship-to-the-spur-telemetry-standard)
5. [Requirements](#5-requirements)
6. [Conformance assessment](#6-conformance-assessment)
7. [The SPUR conformance mark](#7-the-spur-conformance-mark)
8. [Versioning](#8-versioning)

## Introduction

The SPUR Telemetry standard defines a wire format for reporting how AI agents use content. The format is permissive: an emitter producing well-formed events at any conformance level is conforming to the standard.

This profile is the publisher-facing layer. It names a single accreditation tier - Compliant - and the requirements an implementer must meet to be assessed at it. The requirements describe how telemetry is delivered, not what it contains: events arrive at event granularity, in real time, at an endpoint the publisher chooses. The profile makes no requirement about query intent, topic classification, or any other field that would describe what a user asked.

Implementers that receive telemetry and redistribute it to publishers - attribution consumers - meet a parallel set of requirements (section 5.5) that carries these same delivery properties through to the publisher.

The framing is deliberate. When a user accesses a publisher's web page through a CDN, that fetch generates a log line on the publisher's infrastructure. When an AI agent retrieves the same content, the analogous event is the unit of measurement this profile asks for. The standard supports richer disclosure; publishers are free to negotiate it in individual deals. The profile sets the value-neutral baseline.

The standard and this profile are maintained separately. The standard defines the format; this profile defines the publisher-facing requirements layered on it. This profile adds requirements; it never modifies the wire format.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

## 1. Scope

This document specifies:

- the requirements an implementer must meet to be assessed as SPUR Compliant
- how an implementer is assessed against those requirements
- the conditions for displaying the SPUR conformance mark

This document does not specify:

- the telemetry wire format - event types, schema, conformance levels, transport (see the SPUR Telemetry Specification, the normative reference in section 2)
- attribution algorithms or counting models
- content access, licensing, or pricing terms
- privacy policies or data protection requirements

## 2. Normative references

| Reference | Description |
|-----------|-------------|
| SPUR Telemetry Specification, version 0.1 | The telemetry wire format this profile constrains. <https://github.com/SPUR-Coalition/telemetry> |
| RFC 2119 | Key words for use in RFCs to indicate requirement levels |
| RFC 8174 | Ambiguity of uppercase vs lowercase in RFC 2119 key words |

This profile constrains a fixed version of the SPUR Telemetry Specification. Where this document refers to "the standard", it means version 0.1 as cited above. Adoption of a later standard version is a deliberate revision of this profile (section 8).

## 3. Terms and definitions

The terms defined in the SPUR Telemetry Specification section 3 apply. In addition, for the purposes of this document:

### 3.1

**profile**

document that layers community-specific requirements on a standard

### 3.2

**Compliant**

named tier of accreditation under this profile - meeting every requirement in section 5

### 3.3

**accredited implementer**

emitter or attribution consumer assessed as meeting this profile's requirements

### 3.4

**conformance mark**

visual mark a SPUR-accredited implementer may display to indicate Compliant status (section 7)

### 3.5

**publisher-designated endpoint**

destination chosen by a publisher to receive telemetry about that publisher's content

## 4. Relationship to the SPUR Telemetry standard

The standard defines the wire format. This profile selects from it and adds delivery requirements.

The standard defines three conformance levels - Retrieval, Grounding, and Attribution (standard, section 5.7) - and a privacy mechanism with four levels (standard, section 5.5). The standard makes no conformance level and no privacy level mandatory for any relationship.

This profile builds on the standard's mechanisms without changing them. An implementer that meets this profile's requirements is, by construction, conforming to the standard. An implementer can conform to the standard without engaging with this profile at all.

The dependency runs one way - profile to standard, never the reverse. The standard can therefore be transferred to another steward without disturbing this profile: the profile updates its section 2 reference to the standard's new location and version.

## 5. Requirements

An implementer assessed as SPUR Compliant MUST meet every requirement below.

### 5.1 Conformance to the standard

The implementer MUST be a conforming emitter to the SPUR Telemetry Specification at any conformance level - Retrieval, Grounding, or Attribution. Conformance is verified against the standard's reference test suite (standard, section 5.7).

A CDN reporting fetch events from edge servers qualifies at the Retrieval level. An AI platform reporting the full lifecycle from retrieval through engagement qualifies at the Attribution level. Both are SPUR Compliant under this profile; the profile makes no distinction between conformance levels.

### 5.2 Event-level delivery

Telemetry MUST be delivered at event granularity. Each fetched, grounded, cited, displayed, or engaged content piece is reported as a discrete event, with the fields the standard requires at the implementer's conformance level.

Aggregated reporting - summaries, counts, or rollups that collapse multiple events into a single record - does not satisfy this requirement. Aggregation, where useful, is performed by the receiving party on event-level input.

### 5.3 Real-time delivery

The implementer MUST be capable of delivering telemetry in real time. Real-time means events are dispatched to the receiving endpoint as they occur, subject only to ordinary network and processing latency.

A publisher MAY negotiate an alternative delivery cadence (for example, batched delivery on a fixed interval) in a specific commercial agreement. The standard supports both modes; this profile sets real time as the default and lets bilateral agreements vary it.

### 5.4 Publisher-designated endpoint

Telemetry about a publisher's content MUST be able to reach a destination of that publisher's choice. It is not locked to a single party.

This is an outcome requirement, not a fixed delivery path. How an implementer discharges it depends on what it is:

- **Publisher-side emitter** (source role `origin` or `edge`). The emitter delivers events to an endpoint the publisher configures. Endpoint configuration is a per-publisher property: an emitter reporting on content from multiple publishers MUST be able to route events to different endpoints according to the originating publisher's instructions.
- **Agent emitter.** The standard provides no channel for a publisher to instruct an agent where to send session documents; agent routing is governed by the agent's own telemetry configuration (standard, section 7.3). An agent therefore discharges this requirement by sending sessions to an attribution consumer that resolves publisher identity and delivers each publisher's events to a destination that publisher chooses. A consumer relied on for this purpose MUST itself meet this profile's requirements for attribution consumers (section 5.5).

This keeps the guarantee meaningful for the agent path: a publisher cannot dictate which consumer an agent sends to, so the portability promise is carried by the requirement that any such consumer be accredited and honour the publisher's endpoint choice.

### 5.5 Attribution consumer requirements

Sections 5.1 through 5.4 govern emitters. An attribution consumer - a party that receives telemetry and exposes per-publisher views (standard, section 7.3) - is assessed against the requirements below. The agent path in section 5.4 relies on them.

#### 5.5.1 Conformance to the standard

The consumer MUST meet the attribution-consumer conformance rules of the SPUR Telemetry Specification (standard, section 5.7): accept any session with a compatible schema version, tolerate unknown fields and events from any conformance level, accept both the session-document and standalone-event delivery formats and reconstruct sessions from standalone events, and strip privacy-violating fields rather than reject the document carrying them.

#### 5.5.2 Publisher resolution and isolation

The consumer MUST resolve the owning publisher for each event and expose to a given publisher only the events about that publisher's content. A publisher's identifiable telemetry MUST NOT be disclosed to another party without that publisher's authorisation.

Aggregate or anonymised reporting across a catalogue - benchmarks that do not reveal an individual publisher's content usage - is not restricted by this requirement. The bar is on disclosing one publisher's identifiable usage to another, not on a consumer reporting market-level statistics.

This isolation is what lets an agent send a complete multi-publisher session to a single consumer without exposing one publisher's content usage to another.

#### 5.5.3 Onward delivery to a publisher-designated endpoint

The consumer MUST be capable of delivering each publisher's events to a destination of that publisher's choice, at event granularity (as in section 5.2) and in real time (as in section 5.3). A publisher MAY negotiate an alternative cadence, as in section 5.3. This is the property section 5.4 relies on for the agent path.

## 6. Conformance assessment

An implementer is assessed as SPUR Compliant when it meets every requirement in section 5 that applies to it: an emitter against sections 5.1 through 5.4, an attribution consumer against section 5.5. Assessment has two parts:

1. **Technical conformance** - verified against the standard's reference test suite, for the conformance level an emitter advertises (5.1) or against the standard's attribution-consumer rules for a consumer (5.5.1). An objective, repeatable check.
2. **Operational requirements** - the emitter delivery requirements (sections 5.2 through 5.4) and the consumer resolution, isolation, and onward-delivery requirements (sections 5.5.2 and 5.5.3), verified by inspection of the implementer's pipeline and by attestation.

The [`accreditation/`](./accreditation/) directory holds example fixtures: telemetry documents that do and do not satisfy the standard-conformance component of this profile. Operational requirements - cadence, granularity, endpoint configuration, and publisher isolation - cannot be fixture-tested and are assessed separately.

Assessment is self-attested in this preview version. An independent audit programme is anticipated; the profile will be revised to require opt-in to it once available.

## 7. The SPUR conformance mark

A SPUR-accredited implementer may display the SPUR conformance mark.

- The mark indicates the implementer is assessed as SPUR Compliant.
- The mark refers to a specific version of this profile. An implementer reassessed against a later profile version updates the mark accordingly.
- The SPUR Coalition may withdraw the right to display the mark from an implementer that no longer meets the requirements.

The conformance mark is a trademark of the SPUR Coalition. Permission to display it is granted through accreditation and is separate from the [Mozilla Public License 2.0](./LICENSE) that covers this document. The MPL does not grant any right to use the mark or other SPUR trademarks; that right is conveyed only through accreditation.

Mark artwork and detailed display rules are published separately by the SPUR Coalition.

## 8. Versioning

This profile is versioned independently of the standard it constrains.

Preview versions (0.x) may change the requirements as the accreditation programme develops. From 1.0 onward, a change that adds, removes, or materially alters a requirement is a major version change.

This profile constrains a fixed version of the standard (section 2). When the SPUR Telemetry standard publishes a new version, the working group decides whether this profile adopts it. Adoption is a deliberate revision: the section 2 reference changes, and the change is published as a new profile version. The standard advancing does not change this profile until the profile is revised to follow it.

If stewardship of the standard transfers to another body, this profile updates its section 2 reference to the standard's new name and location. The requirements are unaffected - they reference conformance levels and event semantics, which are properties of the format, not of its steward.
