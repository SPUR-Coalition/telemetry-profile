# Accreditation programme consultation

> **Draft for review — not adopted.** This branch proposes changes to Content
> Telemetry Profile 0.2. Consultation has not opened. Participation, installing
> a plugin or passing tests does not confer accreditation or use of the mark.

**Draft:** 15 September 2026. **Status:** Review before publication.
**Comment period:** Dates to be announced. **Proposed version:** 0.3-draft;
published 0.2 remains in force until adoption.

## The publisher promise

A publisher can require reporting as part of an engagement and designate its
reporting destination. The intermediary may offer its own reporting service as
the default. The publisher must have access to its event-level reports and be
able to extract them in the agreed Content Telemetry format or have them
delivered to another designated service.

The programme proposes one Compliant tier with independent assessment of a
named service and configuration. Intermediaries report what they supply and
arrange reporting; agents report their retrieval and subsequent use; telemetry
consumers provide publisher access, isolation and delivery. These functions
can be supplied by different operators. Publishers need not run an endpoint,
and intermediaries need not build their own reporting infrastructure.

This consultation covers reporting and its proposed assessment within the wider
**content market interoperability pilots convened by SPUR**. The aim of those
pilots is to demonstrate an end-to-end market for content in AI systems, from
discovery and authorised access through agreed terms, use and reporting. SPUR
convenes participants and stewards technical standards; independent participants
operate services and make commercial agreements. Pilot plans and participation
remain to be agreed.

The reporting profile does not determine content entitlement, ownership, prices
or compensation. A PoC helps design the programme; an award would require the
adopted requirements and an independent decision.

## Start with one reporting path

**To join:** name a technical contact, describe one interface or agent
integration, and bring a reporting question. An API walkthrough or incomplete
implementation is useful. No fixture pass, production integration, assessor or
accredited dependency is required. When consultation opens, use the Profile
feedback issue form or the announced private technical-session route; a short
description is enough and maintainers can map it to requirements.

**Before the first run:** agree one bounded path, a small authorised test
catalogue, a reporting condition, the publisher's destination and an adapter
between the actual API and test records. Agree the time budget and the question
the experiment will answer. Use an existing authenticated test identity;
Web Bot Auth and the provisional per-item metadata can be separate experiments.
Supported publisher-control formats and precedence must be explicit for the run.

**Demonstrate first:**

1. Acquire or supply one item with its content identity and reporting condition.
2. Deliver its retrieval report to the agreed reporting service. For an
   intermediary path, compare independently captured supply, the intermediary's
   index observation and the agent's retrieval observation.
3. Let the publisher retrieve its event-level report in Content Telemetry format
   from the default hosted service, then designate another destination and check
   delivery there. A receiver acknowledgment alone does not prove publisher access.
4. Repeat a content delivery and retry a report, distinguishing new occurrences
   from duplicate transport attempts.

Add two-publisher isolation, an unmet condition and a temporary outage in the
next run. Where host access permits, add grounding, citation and cached reuse.
Record incomplete capabilities and unexpected costs as design findings. The
full role assessment procedures are for a later award, not prerequisites for
these experiments. A PoC can stop after answering its agreed question.

### Shared support

SPUR proposes to coordinate an acquiring test agent, a test consumer with
publisher access/export, synthetic publisher sites and capture tools. Operators,
funding and availability must be arranged before offering a scheduled run.
Participants contribute their chosen integration and observations; they need
not assemble the whole test environment or adopt a particular vendor's plugin.

SPUR maintains the public reporting contracts, test expectations and adopted
assessment records. Hosted services and plugins may be independently operated,
licensed or commissioned. Their implementation ownership and commercial terms
are separate agreements; contribution to the protocol grants no rights to a
provider's implementation. Service operation does not confer assessment authority.
The test interfaces must support independent agents and consumers.

## Choices participants can change

The role documents and fixtures specify candidate award rules, including choices
still open below. They make proposals testable; participants are not asked to
implement all of them before proposing alternatives. Changing a choice means
updating the requirement, assessment and affected fixtures together.

| ID | Decision and current proposal | What PoCs should establish |
|---|---|---|
| Q1 | Retain one Compliant tier with named roles and scope. | Can publishers understand the assessed promise without extra badge tiers? |
| Q2 | Citation is the candidate minimum for agents, not intermediaries. An alternative is a declared reporting level tied to the assessed relationship. | Which host boundaries can implementers observe? Does a universal Citation floor exclude useful services or protect an essential downstream-use promise? |
| Q3 | Refuse unmet conditions; honour explicit publisher-authorised failure handling and bounded outage recovery. | What buffering limits, deadlines, use restrictions and suspension triggers preserve the promise? No silent loss or invented reports. |
| Q4 | Complete reporting within an enforceable, declared integration; no post-hoc exclusions or bypass. | What is the smallest useful boundary, and which evidence establishes it without inspecting unrelated host activity? |
| Q5 | Keep a complete intermediary supply ledger and currently require complete index-event delivery. Permit delegated reconciliation. | Is full external index-event delivery necessary when the ledger remains complete, or should publisher-agreed sampling apply there too? What receipts let a supplier act without duplicating the consumer? |
| Q6 | Preserve conditions and source identity; use provisional supplier/per-item delivery metadata in adapters. | Which format can independent implementations exchange, including cache reuse and retries? No final API shape is adopted. |
| Q7 | Use licence bindings for reporting demands; core 1.0 manifests cannot express them. | Is a manifest demand hook needed? Propose it in the owning standard without reinterpreting emitter capability fields. |
| Q8 | Web Bot Auth revision 00 is the candidate award mechanism; authenticated existing interfaces suffice for initial PoCs. | Is universal signing justified on authenticated APIs? Agree supported publisher-control formats, discovery and precedence before adoption. |
| Q9 | Independent assessment, with first consumers assessed against section 5.5 directly. | Who operates shared tests and appoints assessors? Resolve funding/conflicts, component-evidence reuse, validity, appeals and withdrawal. |
| Q10 | Public scope, results, material findings and synthetic examples; detailed operational evidence may be private. | What evidence is sufficient and affordable? Agree material-change triggers and proportionate reassessment. |
| Q11 | Privacy levels restrict disclosure; permitted fields are not all required. | Check binding interpretation against core privacy rules and actual publisher needs. |
| Q12 | Publisher-approved hosted access with self-service event export can satisfy the default; publishers can choose onward delivery instead. | Can a publisher retrieve complete portable events and change destination without bespoke assistance? Agree access, retention, freshness and recovery terms. |

## How experience changes the draft

For each PoC, maintainers and participants identify the question being tested,
record implementation effort, missing capabilities and outcomes, then agree a
publishable summary. Maintainers link the evidence to the affected requirement
and record a decision to retain, amend, defer or delete it, with reasons and
remaining disagreement. Revised interfaces are tried across independent
implementations before adoption. Maintainers publish a feedback-resolution
summary and an updated draft before seeking adoption.

When consultation opens, design comments go in the **Profile feedback / open
question** issue form; wording comments can go on the draft pull request.
Question IDs and implementation examples help but are not required for initial
participation. Follow-up pull requests target `accreditation-design` and follow
the repository's [contribution terms](CONTRIBUTING.md#licensing).

Keep credentials, confidential terms, production traces and detailed audit
evidence in agreed private channels. Publish synthetic examples or authorised
summaries. Development sessions are not formal assessments; their debugging
history does not automatically become an applicant's public assessment record.
Outreach and internal coordination belong outside this standards repository.

## Read for your role

- **Intermediaries:** [requirements](accreditation/intermediaries/REQUIREMENTS.md),
  then the [assessment](accreditation/intermediaries/ASSESSMENT.md) when preparing
  an award application.
- **Agents:** [requirements](accreditation/agents/REQUIREMENTS.md), then the
  [assessment](accreditation/agents/ASSESSMENT.md). Retrieval-only PoCs can inform Q2.
- **Consumers and assessors:** [PROFILE.md section 5.5](PROFILE.md#55-telemetry-consumer-requirements)
  and [consumer assessment](accreditation/README.md#consumer-assessment-and-bootstrap).
- **API implementers:** [licence bindings](bindings/README.md) and the role
  [fixture guides](accreditation/README.md#role-programmes).

## Before adoption

Resolve the choices above, agree interoperable reporting formats and supported
control mechanisms, appoint the decision authority and establish first-consumer
assessment, review periods, appeals and withdrawal. Update the profile,
references, procedures and fixtures together through the release process.
