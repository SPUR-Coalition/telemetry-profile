# Accreditation assessment and fixtures

> **Draft for consultation; not adopted.** See the [consultation status](../CONSULTATION.md).

The proposed programme combines standard conformance tests, role-specific
fixtures, independent live tests, operational inspection and attestation.
[PROFILE.md section 6](../PROFILE.md#6-conformance-assessment) defines the
assessment and decision process.

## Role programmes

| Role | Requirements | Assessment procedure | Fixture documentation |
|---|---|---|---|
| Agent | [A1–A10](agents/REQUIREMENTS.md) | [Agent assessment](agents/ASSESSMENT.md) | [Fixture guide](agents/fixtures/README.md) |
| Intermediary | [I-01–I-13](intermediaries/REQUIREMENTS.md) | [Intermediary assessment](intermediaries/ASSESSMENT.md) | [Fixture guide](intermediaries/fixtures/README.md) |

The fixtures check reporting conditions, coverage declarations, refusal and
exception records, publisher exports and reconciliation of deliveries with reports.
Live assessment must establish that the implementation performs the reported behaviour.

## Run the fixtures

From the repository root, using Python 3.9 or later:

```sh
python3 accreditation/validate.py
python3 accreditation/agents/fixtures/run.py
python3 accreditation/intermediaries/fixtures/validate.py
```

These runners need no dependencies or network access. Exit 0 means every
fixture produced its expected result, including the negative cases.

## Existing Retrieval tests

`validate.py` retains the six fixtures from profile 0.2. It rejects incompatible
versions and the withdrawn `content_displayed` event, then checks the required
Retrieval fields: event type, timestamp, content identifier and `source_role`.

| Fixture | Expected result | Check |
|---|---|---|
| `retrieval-standalone-edge` | Pass | Standalone edge retrieval |
| `retrieval-session-edge` | Pass | Session containing retrieval events |
| `grounding-intent-privacy` | Pass | Retrieval requirements within a Grounding session |
| `citation-full-lifecycle` | Pass | Retrieval requirements within a Citation session |
| `retrieval-missing-source-role` | Fail | Missing retrieval source role |
| `retrieval-missing-content-identifier` | Fail | Missing content identifier |

Each fixture has `_test_description` and `_test_expected_tier` annotations.
The latter retains the historical values `"compliant"` and `null`. Here those
values mean a Retrieval test pass or failure, not an accreditation decision.
The proposed agent role also requires Citation capability and operational
assessment.

## Standard schema and application checks

With the standard checked out at `v1.0` and its documented
`jsonschema[format-nongpl]` dependencies available, run:

```sh
python3 -B accreditation/validate_schemas.py /path/to/telemetry
python3 -B accreditation/validate_role_schemas.py /path/to/telemetry
```

The first checks the original six fixtures. The second checks telemetry,
manifest and binding examples in positive role cases. It supplies test
envelopes for event fragments. Negative role cases are checked by the role
runners: a valid telemetry document can still fail an assessment rule.
CI runs these checks against `v1.0` and runs all three fixture suites.

## Consumer assessment and bootstrap

The first consumer can be independently assessed against PROFILE.md section 5.5
using controlled emitters, without an already accredited agent or intermediary.
The programme must appoint the assessor and decision authority before awards.
Test consumers remain usable for PoCs while that process is established.

For each offered reporting arrangement, the assessor must:

1. Pin the service/configuration and verify the standard's consumer rules:
   session, standalone and batch input; compatible versions; unknown fields and
   events; required privacy filtering. Check the standard suite and actual ingress.
2. Register two controlled publishers using verified domains and identifier
   prefixes. Test conflicts and unresolved owners. Compare each publisher's
   events against independently captured input; no cross-publisher context may leak.
3. Test event-level onward delivery, destination changes, duplicate retries,
   outages and recovery. Measure dispatch, receipt and any loss separately.
4. If hosted access is offered, record publisher approval of the default, cadence,
   retention and recovery terms. Authenticate as each publisher, retrieve all
   pages of portable Content Telemetry documents and compare
   identities, references and extensions with input after required privacy filtering.
   Test unauthorised access, delegation/revocation where offered, and availability across the agreed retention
   period. Switch from hosted access to an external endpoint and verify delivery.
5. Where reconciliation is offered, suppress an agent report and verify a
   correlated exception notice, the supplier's response and underlying evidence.
   Confirm that the recipient sees only the data it is authorised to receive.

Use synthetic content. Publisher-access fixtures check normalised record
comparisons; live tests must establish authentication, freshness, retention,
portability and real publisher access. Ingest success alone is insufficient.
Record results under PROFILE.md section 6, using the public record below.

## Public assessment record

Publish a versioned, assessor-signed record identifying:

- The service, assessed roles/configuration, versions and bounded scope, including
  limitations and negotiated reporting arrangements.
- Assessor independence, funding, decision authority, assessment/review dates and
  the correction, appeal and withdrawal procedure once adopted.
- Per-requirement results, material findings, remediation and retests; referenced
  component assessments and the additional integration checks performed.
- Publisher access/delivery results and a reproducible synthetic example with
  scripts, expected/actual records, timing parameters, versions and evidence digests.
- Methods and limits of private operational inspection and supporting attestation.

The assessor retains the detailed formal assessment evidence, including failures,
for inspection. A public summary can link an existing reusable test bundle rather
than republish it. Publish material findings and their resolution; development
sessions do not automatically become a public failure history. Do not publish
credentials, confidential terms or operational records without authority.

## Evidence profile

The separate [evidence profile](https://github.com/SPUR-Coalition/telemetry-evidence-profile)
owns optional evidence mechanisms. No such module is required for a PoC or this
candidate assessment. If used, record its version, maturity as published by its
owner, verifier, trust assumptions and the claim supported, following that
module's requirements. Experimental evidence cannot replace required operational
checks. Retrieval corroboration does not prove grounding or completeness.
