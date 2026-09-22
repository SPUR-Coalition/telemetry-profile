# Intermediary assessment

> **Consultation draft; not adopted.** [Status and review](../../CONSULTATION.md).

**Date:** 15 September 2026. Proposed assessment under profile section 6.

This is the candidate award procedure. The
[first PoC](../../CONSULTATION.md#start-with-one-reporting-path) needs only a
bounded interface and the checks relevant to its question, with test services
that need not already be accredited.

## 1. Method and decision

An assessor independent of the implementer MUST evaluate every applicable
requirement in `REQUIREMENTS.md`. Independence, funding and conflicts MUST be
disclosed. Technical results, operational inspection and implementer
attestation MUST be recorded separately. An attestation MUST NOT substitute
for a failed test or unavailable operational evidence.

The assessment MUST identify the service and configuration, profile and
standard versions, API mapping, consumer route and test period. Each
requirement MUST have a `pass`, `fail` or `not_tested` result with evidence. An
optional path recorded as absent MUST have evidence for that decision;
it MUST NOT exclude an in-scope supply path. A mandatory failure or untested
requirement blocks an award. The experimental API fields must be agreed
before adoption.

## 2. Requirement-to-evidence map

| Requirement | Deterministic local check | Operational inspection and independent experiment | Implementer attestation |
|---|---|---|---|
| I-01 Scope | None | Enumerate APIs, feeds, caches, delegated paths and catalogue; compare deployment configuration and sampled supply logs | Inventory completeness and material-change process |
| I-02 Identity | No cryptographic verifier in this suite | Verify captured requests with the pinned identity draft and public directory; test changed signed components, stale signatures and key rotation; inspect non-HTTP receipt identity | All acquisition clients use the assessed identity path |
| I-03 Controls | None | Controlled allow/disallow crawl, AI-use refusal, licence conflict, control lookup failure, refresh and cached-copy cases within the agreed formats; inspect actual acquisition logs | Declared format support and precedence match the implementation |
| I-04 Records | None | Reconstruct each test decision from time-stamped snapshots, refs and authenticated request or feed receipt; inspect retention and control updates | Records cover production acquisition and refusals |
| I-05 Conditions | Configuration vectors check the selected binding fields | Publish a reporting licence and a domain manifest; verify licence endpoint precedence; confirm manifest conformance is not treated as an agent demand | Publisher onboarding supports reporting conditions |
| I-06 Result conditions | Result and configuration vectors check per-item association and unchanged JSON values, including unknown fields | Capture setup and API exchanges; test mixed publishers, excerpts, pagination, caches and versioned references | All supply paths use the assessed result format |
| I-07 Checks before supply | None; preservation is not capability verification | Test insufficient level, unavailable consumer and unresolved condition with and without publisher-authorised alternatives; inspect identity-to-report mapping and recovery bounds | Conditions and authorised failure policies are checked before supply |
| I-08 Reporting service | Pair vectors check supplied-agent and intermediary metadata | Test consumer ingress, delegated reconciliation receipts and notices; verify accreditation and inspect the underlying evidence | Responsibilities and route match the assessed configuration |
| I-09 Isolation | None | Two publishers, URL-only and ID-only events, conflicting registrations, unknown owner, mixed sessions and privacy-violating turn; check both endpoints and access controls | No alternate export or dashboard bypasses isolation |
| I-10 Access and delivery | Publisher-access vectors compare expected events with hosted exports and alternative-destination receipts | Retrieve as the publisher, test delegate permissions, pagination, retention, endpoint switch, outage and recovery | Event availability, portability and disclosed outage/retention practices |
| I-11 Index coverage | Pair vectors check index role and one expected index event per seeded result | Reconcile assessor-observed deliveries with index ledger, including cache hits and repeated content; inspect filters and manifest scope | Every qualifying in-scope delivery is reported with complete coverage |
| I-12 Correlation | Pair vectors check delivery/content joins, wrong roles, missing/extra events and duplicates | Observe identifier allocation across repeated results, retries and publisher acquisition versus onward supply | Identifier lifecycle matches the declared adapter |
| I-13 Remedy | Missing, extra and mismatched pair vectors exercise finding detection | Suppress an agent report; inspect delegated notices or own reconciliation, publisher notification, authorised recovery and suspension at its limits | Reconciliation is operated directly or delegated, with an accountable remedy process |

Schema validity and application-layer conformance MUST also be verified
against the pinned standard schemas and reference suite, at the advertised
emitter level. The [schema checks](../README.md#standard-schema-and-application-checks) run
separately from the role fixtures.

## 3. End-to-end reconciliation experiment

### 3.1 Setup

The assessor controls `publisher_a.example` and `publisher_b.example`, their
registered domain and identifier-prefix mappings, and separate HTTPS telemetry
endpoints. Use synthetic content and credentials. Publish distinguishable
seeded content, a `content_owner` manifest at each domain and versioned
licences with a reporting condition. The first condition requires Retrieval,
`complete` coverage, `real_time` delivery and `minimal` privacy. Give the
licence an endpoint different from the manifest destination to exercise
precedence. A second publisher uses a different condition and destination.

Record the content, declaration snapshots, expected mapping, supply adapters,
test-agent identity and accredited-consumer configuration before the run.
Record the fields used for supplier identity and each result's delivery ID.
Include at least
one identifier-only result, one cache hit, two successive deliveries of the
same content and a mixed-publisher result page.

The assessor MUST set the normal-load latency budget, clock uncertainty,
load, reporting observation window and outage recovery window before the
run. Publish them as test parameters, not as a definition of real time. Inspect
dispatch behaviour for occurrence-triggered delivery; a scheduled batch fails
the default even if its receipts happen to fall inside the test budget.

### 3.2 Exercise

1. Ingest seeded content through each assessed acquisition path. Capture the
   intermediary's signed HTTP requests or authenticated feed receipts. Check
   controls and licence snapshots against the assessor's publisher records.
2. Request the content as an authenticated test agent. Capture the condition
   available before supply and every returned result. Verify content identity,
   grant, terms, configuration, publisher destination, supplying service and
   per-result delivery identifier. Compare inline configurations as JSON values;
   resolve versioned references and compare their preserved content.
3. Have the test agent emit Retrieval reports with `source_role: agent`, its
   own event `id`, the supplied delivery pair and content identifiers.
   Record the supplier in the agreed field. Send to the
   configured accredited consumer, never a full session to each publisher.
4. Capture index reports and agent reports at consumer ingress and each
   publisher endpoint. Collect supply records independently of the candidate's
   telemetry. Compare event IDs and payloads across the route, including
   terms, grant and correlation fields. Document any privacy transformation.
5. Reconcile each observed supplied item with one logical index observation
   and one logical agent retrieval observation using the supplier/delivery
   pair plus content identity.
   Distinguish a retried identical event from a fresh supply. Check missing
   index events, missing agent events, unexpected events, wrong content,
   inconsistent terms, wrong supplier and late arrivals separately. Count
   index and agent observations as corroboration of one delivery. Report all
   unmatched records.
6. Confirm each publisher received both types of observation for its content,
   and no identifiable event or session context from the other publisher.
   Change one publisher's endpoint through the authenticated configuration
   path, deliver new content and verify the new route. Where hosted access is
   offered, start with the publisher-approved intermediary default: authenticate
   as the publisher, retrieve all event pages as Content Telemetry documents and
   compare both observations and their references with consumer ingress. Test an
   authorised delegate and revoke access where delegation is offered. Confirm another publisher's events and
   session context never appear. A dashboard total or an ingress acknowledgment
   cannot substitute for this check. Test a temporary failure
   and recovery, preserving event IDs and recording delay and retries.
7. Repeat with a deliberately insufficient agent capability, unresolved
   declaration and failed reporting route. Without an explicit publisher-authorised
   alternative the candidate must decline affected supply. Repeat with permitted
   acquisition and separately permitted use; confirm that an exception never
   invents agent observations. Test agreed recovery within and beyond its time
   and capacity bounds. Separately suppress a report after successful supply;
   verify a finding, delegated notice where applicable, remedy and suspension
   when the condition or recovery limits require it.
8. Where supplied licences demand Grounding or Citation, drive qualifying
   agent behaviour and check the required lifecycle reports at the endpoint.
   Treat those records as agent observations; do not infer them from an index
   match. Optional presentation and engagement require separate checks when
   included in the declared relationship.

### 3.3 Decision and limits

Under the complete-coverage Retrieval test, every deliberately completed test
delivery MUST have both logical observations available through the publisher's
agreed hosted access or at its chosen endpoint within the observation window.
Test freshness against availability, not the time the publisher elects to download.
Missing, unexpected, mismatched or
late records are findings. In fault cases, record both the injected fault and
the required response; an expected injected missing report tests detection,
not successful ordinary delivery. Resolve unexplained findings before passing.

The experiment covers the tested paths and period. The assessor also needs
pipeline inspection and attestation to assess production completeness.
Retrieval matches do not prove grounding or licence validity.

## 4. Evidence profile

The shared [evidence guidance](../README.md#evidence-profile) applies. The
assessor MUST record which mechanisms were used and what each result supports.
The seeded content in this procedure is a controlled test input; its use does
not claim conformance to an unfinished evidence module.

## 5. Public assessment record

Use the shared [public assessment record](../README.md#public-assessment-record).
For intermediaries, identify supply interfaces, catalogue scope, the API mapping,
consumer and delegated responsibilities. Include a synthetic supply-to-publisher
reconciliation, hosted access/export results where offered, destination-change
results and the treatment of missing reports and authorised recovery.

Apply PROFILE.md section 6.3 for material-change review and component reuse.
Confidential operational records may remain private; the public summary must
state what was inspected and its limits.
