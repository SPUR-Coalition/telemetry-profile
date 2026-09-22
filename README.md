# SPUR Content Telemetry Profile

> **Accreditation consultation draft — not adopted.** The
> `accreditation-design` branch proposes changes to the published 0.2 profile.
> Requirements may change. Consultation has not opened. Participation or
> passing tests does not confer accreditation or permission to use the mark.

A publisher can require reporting as part of an engagement and designate its
reporting destination. The intermediary may offer its own reporting service as
the default. The publisher must have access to its event-level reports and be
able to extract them in the agreed Content Telemetry format or have them
delivered to another designated service.

## Content market interoperability pilots convened by SPUR

SPUR acts as a technical standards organisation and convener. The wider aim is
to demonstrate an end-to-end market for content in AI systems: discovery,
authorised access, agreed terms, use and reporting across independent services.
Participants operate those services and make their own commercial agreements.
SPUR develops interoperable standards so the market can develop independently.

This draft addresses the reporting and assessment part of that work. It does
not establish a SPUR-operated marketplace or reporting service. Pilot plans,
participants and service availability remain to be agreed.

## Help design the programme

Start with [the first PoC](CONSULTATION.md#start-with-one-reporting-path).
Bring one interface or agent integration and a question you want to test.
An API walkthrough or an incomplete implementation is enough to join; you do
not need an assessor, an accredited consumer or a passing fixture suite.
SPUR proposes to coordinate shared test services so participants can work on
their own integration. Service availability and operators remain to be arranged.

## Review this draft

[CONSULTATION.md](CONSULTATION.md) lists the changes and questions for review.
The draft retains one **Compliant** tier, with requirements for each service role.

| Document | Purpose |
|---|---|
| [PROFILE.md](PROFILE.md) | Proposed profile requirements, assessment and mark scope |
| [Intermediary requirements](accreditation/intermediaries/REQUIREMENTS.md) | Acquisition controls, reporting conditions, supply records and onward reports |
| [Agent requirements](accreditation/agents/REQUIREMENTS.md) | Identity, reporting conditions, retrieval, grounding, citation and consumer routing |
| [Assessment and fixtures](accreditation/README.md) | Independent verification procedures and reproducible positive/negative vectors |
| [Licence bindings](bindings/README.md) | How a licence carries a reporting condition and publisher destination |
| [Contributing](CONTRIBUTING.md) | Feedback, change proposals and contribution terms |

Citation remains the proposed agent assessment target; whether it should be
the minimum for every agent is open in Q2. Retrieval-only PoCs are welcome.
Intermediaries report their supplies and arrange the reporting service; agents
report their use; consumers provide publisher access and routing. Supplying
an agent does not make an intermediary an agent. A service performing multiple
roles is assessed against the requirements of those roles.

## Relationship to the standard

The wire format lives in [SPUR-Coalition/telemetry](https://github.com/SPUR-Coalition/telemetry).
A [TypeScript SDK](https://github.com/SPUR-Coalition/telemetry-js) provides document
builders and an optional HTTP adapter; its README explains the v1 source build.
Using an SDK does not confer accreditation.

This profile constrains Content Telemetry 1.0 and does not change its event
semantics. Experimental supplier and per-item delivery metadata is explicitly
marked in the role fixtures; their final format remains open for review.

The profile governs reporting and observance of declared reporting conditions.
It does not decide content entitlement, ownership, pricing or compensation.

## Run the draft fixtures

These examples explain the proposed checks. Connecting your implementation
starts with the PoC above; running these files is not an entry requirement.

From the repository root, using Python 3.9 or later with no dependencies:

```sh
python3 accreditation/validate.py
python3 accreditation/agents/fixtures/run.py
python3 accreditation/intermediaries/fixtures/validate.py
```

The suites check synthetic records and deterministic assessment rules. Full
standard conformance and operational behaviour require the additional checks
in [accreditation/](accreditation/README.md).

## Version and status

Proposed version **0.3-draft**. Published preview **0.2** remains in force
until adoption.
