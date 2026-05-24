# Accreditation fixtures

Tier fixtures for the SPUR Telemetry Profile, and the runner that assesses them.

These verify the two objective components of a tier — the technical baseline and the privacy floor (PROFILE.md sections 5 and 6). Behavioural commitments are assessed separately (PROFILE.md section 7) and cannot be fixture-tested.

## Layout

```
accreditation/
  validate.py    the tier-assessment runner
  fixtures/      SPUR Telemetry documents, each declaring its expected tier
```

## Running

```sh
python3 validate.py
```

No dependencies. Exit code 0 means every fixture was assessed at its expected tier. The runner also works under uv:

```sh
uv run validate.py
```

## How a fixture is assessed

Each fixture is a SPUR Telemetry document — a session document or a standalone event. The runner computes the highest tier the document reaches:

1. **Technical baseline** — the conformance level the document satisfies (standard, section 5.7): Retrieval, Grounding, or Attribution.
2. **Privacy floor** — whether every conversation turn carries a `privacy_level` at or above the tier's floor (PROFILE.md section 6).

A document is assessed at the highest tier whose baseline and floor it both meets. A grounding-conformant session whose turns are all at `minimal` privacy meets the Grounding baseline but fails the `intent` floor, so it is assessed at Compliant — not Preferred.

The runner checks tier assignment. It assumes fixtures are well-formed SPUR Telemetry documents; validating a document against the JSON Schema is the [standard repository's](https://github.com/SPUR-Coalition/telemetry) test suite.

## Fixture format

Each fixture carries two annotation fields alongside the telemetry document:

- `_test_description` — what the fixture demonstrates
- `_test_expected_tier` — the tier the document should be assessed at: `"compliant"`, `"preferred"`, `"strategic"`, or `null` when the document reaches no tier

SPUR Telemetry consumers tolerate unknown fields, so these annotations do not affect the document's validity. The runner asserts that each fixture's assessed tier equals its `_test_expected_tier`.

## What the suite covers

| Fixture | Expected | Demonstrates |
|---------|----------|--------------|
| `retrieval-standalone-edge` | Compliant | Standalone CDN retrieval event |
| `retrieval-session-edge` | Compliant | Session of retrieval events only |
| `grounding-minimal-privacy` | Compliant | Grounding baseline met, but below the intent floor |
| `grounding-missing-agent-id` | Compliant | Grounding baseline fails on a missing session field |
| `grounding-intent-privacy` | Preferred | Grounding baseline plus the intent floor |
| `grounding-summary-privacy` | Preferred | Summary clears the intent floor |
| `attribution-cited-no-citation-type` | Preferred | Attribution baseline fails on a missing citation field |
| `attribution-privacy-gating-violation` | Preferred | Attribution baseline fails on the privacy gating rule |
| `attribution-full-lifecycle` | Strategic partner | Full retrieval-to-engagement lifecycle |
| `attribution-summary-privacy` | Strategic partner | Attribution with summarised text |
| `retrieval-missing-source-role` | No tier | Retrieval baseline fails on a missing field |
| `retrieval-missing-content-identifier` | No tier | Retrieval baseline fails — no content identifier |

## Behavioural commitments

The behavioural commitments in PROFILE.md section 5 — published completeness figures, audit opt-in, working group participation, the public interoperability commitment — are verified by attestation and published evidence during accreditation. They are not represented in these fixtures.
