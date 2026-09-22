# SPUR Content Telemetry Profile

> **Accreditation consultation draft — not adopted.** This branch proposes
> changes to the published 0.2 profile. Requirements may change; consultation
> has not opened. Participation or passing tests does not confer accreditation
> or permission to use the conformance mark. See [the review guide](CONSULTATION.md).

Publisher-facing requirements for the Content Telemetry standard.

**Version:** 0.3-draft (based on 0.2)
**Status:** Consultation draft — not adopted
**Last updated:** 2026-09-15
**Constrains:** Content Telemetry Specification, version 1.0

## Contents

1. [Scope](#1-scope)
2. [Normative references](#2-normative-references)
3. [Terms and definitions](#3-terms-and-definitions)
4. [Relationship to the Content Telemetry standard](#4-relationship-to-the-content-telemetry-standard)
5. [Requirements](#5-requirements)
6. [Conformance assessment](#6-conformance-assessment)
7. [The SPUR conformance mark](#7-the-spur-conformance-mark)
8. [Versioning](#8-versioning)

## Introduction

This profile defines the Compliant accreditation tier for Content Telemetry
implementers. It requires event-level reporting, timely publisher access and
a reporting destination chosen by each publisher. It does not require query
text, intent or topic classification.

Requirements depend on the service's role: emitter, telemetry consumer,
intermediary or agent. Services performing more than one role meet all
applicable requirements. The profile adds requirements without changing the
standard's wire format or event meanings.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

## 1. Scope

This document specifies:

- the requirements an implementer must meet to be assessed as SPUR Compliant
- how an implementer is assessed against those requirements
- the conditions for displaying the SPUR conformance mark

This document does not specify:

- the telemetry wire format - event types, schema, conformance levels, transport (see the Content Telemetry Specification, the normative reference in section 2)
- attribution algorithms or counting models
- content access, licensing, or pricing terms
- privacy policies or data protection requirements

## 2. Normative references

| Reference | Description |
|-----------|-------------|
| Content Telemetry Specification, version 1.0 | The telemetry wire format this profile constrains. <https://github.com/SPUR-Coalition/telemetry> |
| RFC 2119 | Key words for use in RFCs to indicate requirement levels |
| RFC 8174 | Ambiguity of uppercase vs lowercase in RFC 2119 key words |
| RFC 9421 | HTTP Message Signatures, used by the role-specific request identity requirements. <https://www.rfc-editor.org/rfc/rfc9421> |
| draft-ietf-webbotauth-httpsig-protocol-00 | HTTP Message Signatures for automated traffic, 1 September 2026; work in progress, pinned for this consultation. <https://datatracker.ietf.org/doc/html/draft-ietf-webbotauth-httpsig-protocol-00> |
| RFC 9309 | Robots Exclusion Protocol, used by the intermediary acquisition requirements. <https://www.rfc-editor.org/rfc/rfc9309> |

This profile constrains a fixed version of the Content Telemetry Specification. Where this document refers to "the standard", it means version 1.0 as cited above. Adoption of a later standard version is a revision of this profile (section 8).

## 3. Terms and definitions

The terms defined in the Content Telemetry Specification section 3 apply. This profile uses *publisher* for what the standard calls a *content owner*; within this document the terms are interchangeable. In addition, for the purposes of this document:

### 3.1

**profile**

document that layers community-specific requirements on a standard

### 3.2

**Compliant**

named tier of accreditation under this profile - meeting every applicable requirement in section 5

### 3.3

**accredited implementer**

service assessed as meeting the requirements applicable to its emitter, telemetry consumer, intermediary or agent roles

### 3.4

**conformance mark**

visual mark a SPUR-accredited implementer may display to indicate Compliant status (section 7)

### 3.5

**publisher-designated endpoint**

destination chosen by a publisher to receive telemetry about that publisher's content

### 3.6

- **Intermediary.** A service that supplies content to agents: a grounding
  or search service, a retrieval API, a marketplace or a licensed feed. It
  acquires or licenses publishers' work and serves it onward. In the
  standard's terms its own observations carry `source_role: index`; where it
  receives agents' reports and redistributes per-publisher views it is also
  a telemetry consumer (standard section 7.3; profile section 5.5). The
  standard's marketplace pattern (SPECIFICATION.md, the paragraph beginning
  "A marketplace operating as both emitter and telemetry consumer") is the
  starting point.

### 3.7

- **Agent.** A system that takes content in and uses it to answer a question
  or complete a task, whether it fetched the content itself or obtained it
  from an intermediary. Its observations carry `source_role: agent`
  (profile section 5.4, agent emitter).
- One company can be both. Each service is assessed in the role it performs.

The **telemetry consumer** receives reports, isolates each publisher's data
and provides access, export and onward delivery. An intermediary MAY delegate
that function and reconciliation to a separate provider. Supplying an agent
does not by itself make the intermediary an agent or require Citation capability.

These source roles describe retrieval observations. They MUST NOT be used to
change the standard's lifecycle semantics or substitute supplier identity for
emitter identity. Accreditation MUST NOT decide entitlement, ownership, price
or compensation. Access evidence MUST NOT be treated as proof of grounding.

## 4. Relationship to the Content Telemetry standard

The standard defines three conformance levels - Retrieval, Grounding, and Citation (standard, section 5.7) - and a privacy mechanism with four levels (standard, section 5.5). The standard makes no conformance level and no privacy level mandatory for any relationship. The standard also separates conformance from coverage: a conformance level proves what an emitter can report, and reporting coverage is a distinct, explicit declaration in one of four modes (standard, section 5.7.6). This profile selects the `complete` mode as its default requirement (section 5.2).

An implementation can conform to the standard without meeting this profile.
An implementation assessed under this profile must meet both.

This profile depends on the standard; the standard does not depend on this profile.

## 5. Requirements

An implementer assessed as SPUR Compliant MUST meet every requirement applicable to the service roles it performs, as set out in section 6.

### 5.1 Conformance to the standard

An emitter MUST conform to the Content Telemetry Specification at Retrieval, Grounding or Citation level. An implementer assessed in the agent role MUST demonstrate Citation conformance, including the cumulative Retrieval and Grounding requirements, under section 5.7. Conformance is verified against the standard's JSON Schemas (standard, Annex A) and its reference test suite for the application-layer conformance rules (standard, section 5.7.5).

A CDN reporting fetch events from edge servers qualifies at the Retrieval level. An AI platform reporting retrieval, grounding, and citation qualifies at the Citation level; presentation and engagement events are optional lifecycle signals under the standard. The Retrieval emitter can meet the emitter requirements. The AI platform is also assessed against the agent requirements. Either must meet all applicable operational requirements before an accreditation decision.

Citation is the candidate agent minimum under consultation question Q2.
Retrieval-only experiments can inform that decision without meeting the full
candidate assessment. These experiments make no accreditation claim.

### 5.2 Event-level delivery

Telemetry MUST be delivered at event granularity. Each fetched, grounded, cited, presented, or engaged content piece is reported as a discrete event, with the fields the standard requires at the implementer's conformance level.

Aggregated reporting - summaries, counts, or rollups that collapse multiple events into a single record - does not satisfy this requirement; in the standard's coverage vocabulary this is the `aggregated` mode. Aggregation, where useful, is performed by the receiving party on event-level input.

Within the scope of the relationship it reports under, the implementer MUST report every qualifying occurrence it observes: `complete` coverage in the standard's terms (standard, section 5.7.6), for every event type it emits - including the optional presentation and engagement lifecycle signals, when the implementer emits them. Selective reporting - the standard's `selected` mode - does not satisfy this requirement. A publisher MAY accept sampling (the standard's `sampled` mode, under its stated sampling rule) in a specific commercial agreement, as with delivery cadence in section 5.3. Except where a role-specific requirement makes the declaration mandatory, the implementer SHOULD declare its coverage machine-readably in its manifest (`telemetry.coverage`; standard, section 8.5). Whether reporting in fact met the declared coverage is assessed as an operational requirement (section 6). The intermediary's own supply ledger MUST have complete coverage under section 5.6; the sampling exception does not apply to that ledger.

### 5.3 Real-time delivery

The implementer MUST be capable of delivering telemetry in real time. Real-time means events are dispatched to the receiving endpoint as they occur, subject only to ordinary network and processing latency.

A publisher MAY negotiate an alternative delivery cadence (for example, batched delivery on a fixed interval) in a specific commercial agreement. The standard supports both modes; this profile sets real time as the default and lets bilateral agreements vary it.

Under the hosted-access arrangement in section 5.5.3, events MUST become
available for publisher retrieval as they occur, subject to ordinary processing
latency, unless the publisher agrees another cadence. The time the publisher
chooses to download them is not dispatch delay. Receipt by the consumer alone
does not establish publisher availability.

### 5.4 Publisher-designated endpoint

Telemetry about a publisher's content MUST be able to reach a destination of that publisher's choice.

A publisher MUST be able to require reporting as part of an engagement with
an intermediary. The intermediary MAY offer its own reporting service as the
default, with the publisher's agreement. The publisher MUST be able to extract
its event-level reports in Content Telemetry format or designate another
service for onward delivery under section 5.5.3. A default MUST NOT override
an explicit publisher destination. An agreed hosted account needs no additional
publisher-operated HTTP endpoint.

The delivery route depends on the service role:

- **Publisher-side emitter** (source role `origin` or `edge`). The emitter delivers events to an endpoint the publisher configures. Endpoint configuration is a per-publisher property: an emitter reporting on content from multiple publishers MUST be able to route events to different endpoints according to the originating publisher's instructions.
- **Agent emitter.** The standard provides no channel for a publisher to instruct an agent where to send session documents; agent routing is governed by the agent's own telemetry configuration (standard, section 7.3). An agent therefore discharges this requirement by sending sessions to a telemetry consumer that resolves publisher identity and delivers each publisher's events to a destination that publisher chooses. A consumer relied on for this purpose MUST itself meet this profile's requirements for telemetry consumers (section 5.5).

- **Intermediary emitter** (source role `index`). The intermediary reports its own deliveries and arranges reporting for the receiving agent under section 5.6. Both observations MUST reach the publisher's agreed hosted account or designated endpoint under section 5.5.3. An intermediary operating the receiving consumer also meets section 5.5.

On the agent path a publisher cannot choose which consumer an agent sends to; the endpoint requirement is instead carried by the rule that any such consumer be accredited and honour the publisher's endpoint choice.

### 5.5 Telemetry consumer requirements

Sections 5.1 through 5.4 govern emitters. A telemetry consumer - a party that receives telemetry and exposes per-publisher views (standard, section 7.3) - is assessed against the requirements below. The agent path in section 5.4 relies on them.

#### 5.5.1 Conformance to the standard

The consumer MUST meet the telemetry-consumer conformance rules of the Content Telemetry Specification (standard, section 5.7.4): accept any document with a compatible schema version (same major version, under the standard's minor-version rules), tolerate unknown fields and events from any conformance level, and accept the session-document, standalone-event, and event-batch delivery formats, reconstructing sessions from standalone events and event batches where needed. The consumer MUST also strip privacy-violating fields rather than reject the document carrying them; the standard recommends this behaviour (standard, section 5.7.5) and this profile makes it a requirement.

#### 5.5.2 Publisher resolution and isolation

The consumer MUST resolve the owning publisher for each event and expose to a given publisher only the events about that publisher's content. A publisher's identifiable telemetry MUST NOT be disclosed to another party without that publisher's authorisation.

Aggregate or anonymised reporting across a catalogue - benchmarks that do not reveal an individual publisher's content usage - is not restricted by this requirement.

#### 5.5.3 Publisher access, export and onward delivery

The consumer MUST be capable of delivering each publisher's events to a destination of that publisher's choice, at event granularity (as in section 5.2) and in real time (as in section 5.3). A publisher MAY negotiate an alternative cadence, as in section 5.3.

With the publisher's agreement, a hosted reporting account MAY satisfy the
engagement through authenticated publisher access and self-service extraction
of event-level Content Telemetry documents. The publisher MUST be able to
retrieve all its reportable events for the agreed retention period, with their
identities, source roles, content and terms references and supported extensions
preserved, subject to required privacy filtering. Aggregate dashboards or a
bespoke export available only by asking the operator are insufficient.

The agreement MUST identify the reporting service, access method, format,
availability cadence, retention and recovery terms. A publisher MUST be able to
change to onward delivery at its designated endpoint through an authenticated
configuration process. A consumer offering delegated access MUST enforce the
publisher's authorisation and revocation. The consumer MUST demonstrate
both hosted access/export and onward delivery if it offers hosted access.
Publisher isolation applies equally to downloads, APIs, delegates and dashboards.

This hosted-access option changes the 0.2 profile's delivery policy; it does
not change the standard's event formats. Its final terms are open in Q12.

### 5.6 Intermediary requirements

A service acting as an intermediary MUST meet
[the intermediary requirements I-01 through I-13](accreditation/intermediaries/REQUIREMENTS.md),
which form part of this draft profile. It MUST meet sections 5.1 through 5.4
for its index observations and section 5.5 where it operates a consumer.

These requirements cover acquisition identity and publisher controls,
recording and carrying reporting conditions, checks before supply, arranging
agent reporting, publisher isolation and access/delivery. Every qualifying
supply occurrence MUST be represented in a complete index ledger. Delegating
the consumer or reconciliation function does not remove accountability for
the intermediary's own supply records and response to reporting failures.

### 5.7 Agent requirements

A service acting as an agent MUST meet
[the agent requirements A1 through A10](accreditation/agents/REQUIREMENTS.md),
which form part of this draft profile, in addition to sections 5.1 through 5.4.

These requirements cover signed acquisition requests, discovery and observance
of reporting conditions, refusal when a condition cannot be met, Citation
capability, complete coverage of the assessed integration, supplying-service
identification and delivery through an accredited consumer. Scope MUST NOT
exclude paths because they failed to report or cannot observe required use.

Both role programmes use the same Compliant tier. The provisional supplier
and delivery extension described in their fixtures is an experimental pilot
interface, not a core field or an adopted interoperability requirement.
Its final format must be agreed before adoption; see
[CONSULTATION.md](CONSULTATION.md).

## 6. Conformance assessment

This section proposes independent assessment. The published 0.2 preview's
self-attestation process remains in force until the revised programme is
adopted. This consultation grants no accreditation.

### 6.1 Applicable requirements

| Assessed role | Requirements | Additional procedure |
|---|---|---|
| Publisher-side emitter | Sections 5.1 through 5.4 | Standard conformance and operational delivery assessment |
| Telemetry consumer | Section 5.5 | Consumer conformance, owner resolution, isolation and onward delivery |
| Intermediary | Sections 5.1 through 5.4 and 5.6; section 5.5 when operating a consumer | [Intermediary assessment](accreditation/intermediaries/ASSESSMENT.md) |
| Agent | Sections 5.1 through 5.4 and 5.7; section 5.5 when operating a consumer | [Agent assessment](accreditation/agents/ASSESSMENT.md) |

A service performing multiple roles MUST meet all their requirements.
An outsourced consumer MUST itself meet section 5.5; its identity, assessed
version and delivery route MUST be available for inspection.

Consumers can be assessed directly against section 5.5 using controlled test
emitters; those emitters need not already be accredited. Establish this route
before the first agent or intermediary award relies on a consumer. The
[consumer procedure](accreditation/README.md#consumer-assessment-and-bootstrap)
describes the tests. Unassessed services can be used in PoCs.

An assessor MAY reuse applicable evidence from an independently assessed
component at the same relevant version and configuration, recording its scope
and limits. The candidate's integration, publisher access and operational
behaviour MUST still be tested. Installing a plugin does not confer an award.

### 6.2 Assessment evidence

Assessment MUST distinguish:

1. **Technical conformance:** the pinned standard's schemas and reference
   application-layer tests at the advertised level, consumer compatibility
   where applicable, and the role-specific deterministic fixtures.
2. **Operational verification:** independent inspection and controlled live
   challenges covering delivery, scope, coverage, publisher isolation and
   reporting-condition observance. Attestation supports this evidence; it
   MUST NOT replace an unperformed or failed required test.

Multi-record fixtures can check reconciliation logic and preservation of
conditions. They cannot establish that an implementation signs requests,
refuses acquisition, dispatches in real time, isolates publishers or reports
all production occurrences. The six original Retrieval fixtures remain a
Retrieval check and MUST NOT be represented as a complete agent assessment.

### 6.3 Independent decision and public record

An assessor independent of the implementer MUST perform the assessment and
disclose funding and relevant conflicts. The implementer MUST NOT determine
its own accreditation result. Each mandatory requirement MUST be recorded
as `pass`, `fail` or `not_tested`, with evidence. Missing evidence and unresolved
mandatory findings block an award. A justified absence of an optional path
MUST be explained, not silently counted as a pass.

The public assessment record MUST identify the service and configuration,
roles, scope, versions, assessor, consumer dependencies, requirement results,
limitations and reproducible synthetic evidence. Confidential operational
evidence MAY be inspected privately; the public record MUST explain the
inspection and its limits without disclosing unauthorised data. Material
changes MUST trigger review before the changed configuration claims the mark.

A material change alters an assessed capability, reporting condition, scope,
identity binding, isolation boundary or delivery guarantee. The implementer
MUST record changes and assess their impact. Review MUST cover affected
requirements and integration checks; unchanged component tests MAY be reused.
Routine key rotation or an endpoint change through an already tested process
does not alone require a fresh full assessment. The assessor MUST inspect that
change process and its records. Review intervals remain to be adopted.

Publish material findings from the formal assessment, their resolution and
retest outcomes. Retain supporting assessment evidence for private inspection.
Exploratory PoC debugging history is not automatically a public assessment record.

Appointment of the decision authority, validity periods, appeals and
withdrawal procedures require programme adoption. The open decisions and
consultation process are recorded in [CONSULTATION.md](CONSULTATION.md).

## 7. The SPUR conformance mark

A SPUR-accredited implementer may display the SPUR conformance mark.

- The mark indicates the implementer is assessed as SPUR Compliant.
- The mark identifies the assessed service, configuration, roles and public assessment record. It MUST NOT imply accreditation of unrelated services or every action of a host.
- The mark refers to a specific version of this profile. An implementer reassessed against a later profile version updates the mark accordingly.
- The SPUR Coalition may withdraw the right to display the mark from an implementer that no longer meets the requirements.

The conformance mark is a trademark of the SPUR Coalition. Permission to display it is granted through accreditation and is separate from the [Creative Commons Attribution-ShareAlike 4.0 International licence](./LICENSE) that covers this document. Consistent with section 2(b)(2) of that licence, the licence grants no right to use the SPUR conformance mark or other SPUR trademarks; that right is conveyed only through accreditation.

Mark artwork and detailed display rules are published separately by the SPUR Coalition.

## 8. Versioning

This profile is versioned independently of the standard it constrains.

Preview versions (0.x) may change the requirements as the accreditation programme develops. From 1.0 onward, a change that adds, removes, or materially alters a requirement is a major version change.

This profile constrains a fixed version of the standard (section 2). When the Content Telemetry standard publishes a new version, the SPUR Coalition decides whether this profile adopts it. Adoption is a revision: the section 2 reference changes, and the change is published as a new profile version. The standard advancing does not change this profile until the profile is revised to follow it.

If stewardship of the standard transfers to another body, this profile updates its section 2 reference to the standard's new name and location. The requirements are unaffected - they reference conformance levels and event semantics, which are properties of the format, not of its steward.
