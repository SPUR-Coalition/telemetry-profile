# Accreditation fixtures

Example telemetry documents for the SPUR Content Telemetry Profile, and the runner that assesses them against the single Compliant tier.

These verify the standard-conformance component of the profile (PROFILE.md section 5.1). The delivery requirements - event-level granularity, real-time delivery, and publisher-designated endpoint (sections 5.2 through 5.4) - are properties of the implementer's reporting pipeline and cannot be fixture-tested. They are assessed separately by attestation and endpoint inspection.

## Layout

```
accreditation/
  validate.py    the assessment runner
  fixtures/      Content Telemetry documents, each declaring its expected outcome
```

## Running

```sh
python3 validate.py
```

No dependencies. Exit code 0 means every fixture was assessed at its expected outcome. The runner also works under uv:

```sh
uv run validate.py
```

## How a fixture is assessed

Each fixture is a Content Telemetry document - a session document or a standalone event. The runner first rejects documents a conforming v1 consumer must reject - a non-v1 `schema_version` (standard, section 5.7.4) or a withdrawn `content_displayed` event (standard, section 12.1) - then checks Retrieval conformance (standard, section 5.7.1): every event has `type` and `timestamp`, every content event carries at least one of `content_url` or `content_id`, and every `content_retrieved` event carries `source_role`.

Retrieval is the standard's least-demanding conformance level, and Grounding and Citation are cumulative on it. Passing Retrieval is therefore necessary and sufficient for the standard-conformance component of this profile.

A document that passes Retrieval is assessed Compliant. A document that fails Retrieval reaches no tier.

The runner assumes fixtures are well-formed Content Telemetry documents; validating a document against the JSON Schema is the [standard repository's](https://github.com/SPUR-Coalition/telemetry) test suite.

## Fixture format

Each fixture carries two annotation fields alongside the telemetry document:

- `_test_description` - what the fixture demonstrates
- `_test_expected_tier` - the outcome the document should be assessed at: `"compliant"` or `null` when the document reaches no tier

Content Telemetry consumers tolerate unknown fields, so these annotations do not affect the document's validity. The runner asserts that each fixture's assessed outcome equals its `_test_expected_tier`.

## What the suite covers

| Fixture | Expected | Demonstrates |
|---------|----------|--------------|
| `retrieval-standalone-edge` | Compliant | Standalone CDN retrieval event |
| `retrieval-session-edge` | Compliant | Session of retrieval events only |
| `grounding-intent-privacy` | Compliant | Grounding-conformant session - the profile is agnostic to privacy_level |
| `citation-full-lifecycle` | Compliant | Citation plus optional presentation and engagement signals |
| `retrieval-missing-source-role` | No tier | Retrieval baseline fails on a missing field |
| `retrieval-missing-content-identifier` | No tier | Retrieval baseline fails - no content identifier |

## Delivery requirements

The delivery requirements in PROFILE.md sections 5.2 through 5.4 - event-level granularity, real-time delivery, and a publisher-designated endpoint - are verified by attestation and endpoint inspection during accreditation. They are not represented in these fixtures.

The telemetry consumer requirements (PROFILE.md section 5.5) are assessed the same way. A consumer's standard conformance (5.5.1) is the consumer-side reading rules of the standard; publisher resolution, isolation, and onward delivery (5.5.2, 5.5.3) are pipeline properties verified by attestation and inspection, not by these fixtures.
