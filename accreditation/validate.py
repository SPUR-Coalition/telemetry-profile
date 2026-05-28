#!/usr/bin/env python3
"""Accreditation assessment for the SPUR Telemetry Profile.

This profile defines a single tier - Compliant - whose technical requirement
(PROFILE.md section 5.1) is that the implementer is a conforming emitter to
the SPUR Telemetry Specification at any conformance level. The cheapest level
to satisfy is Retrieval (standard, section 5.7.1), and Grounding and
Attribution are cumulative on it. Checking Retrieval conformance is therefore
necessary and sufficient for the standard-conformance component of this
profile's assessment.

The delivery requirements - event-level granularity, real-time delivery, and
publisher-designated endpoint (PROFILE.md sections 5.2 through 5.4) - are
properties of the implementer's reporting pipeline and cannot be checked from
a single telemetry document. They are assessed separately by attestation and
endpoint inspection.

No external dependencies. Validating a document against the JSON Schema is the
standard repository's test suite; this runner assumes fixtures are well-formed
SPUR Telemetry documents and assesses whether they reach the Compliant tier.

Usage:
    python3 validate.py
"""

import json
import sys
from pathlib import Path

CONTENT_EVENTS = {
    "content_retrieved",
    "content_grounded",
    "content_cited",
    "content_displayed",
    "content_engaged",
}
VALID_TIERS = ("compliant",)


def events(doc):
    """Yield the document's events, whether it is a session or standalone event."""
    if doc.get("document_type") == "event":
        event = doc.get("event")
        return [event] if event else []
    return doc.get("events", []) or []


def check_retrieval(doc):
    """Retrieval conformance - standard section 5.7.1."""
    fails = []
    for i, event in enumerate(events(doc)):
        etype = event.get("type", "?")
        loc = f"event[{i}] {etype}"
        if "type" not in event:
            fails.append(f"{loc}: missing 'type'")
        if "timestamp" not in event:
            fails.append(f"{loc}: missing 'timestamp'")
        if (
            etype in CONTENT_EVENTS
            and not event.get("content_url")
            and not event.get("content_id")
        ):
            fails.append(f"{loc}: content event needs 'content_url' or 'content_id'")
        if etype == "content_retrieved" and not event.get("source_role"):
            fails.append(f"{loc}: content_retrieved missing 'source_role'")
    return fails


def assess(doc):
    """Return (tier or None, blocking reasons) for a document."""
    fails = check_retrieval(doc)
    if not fails:
        return "compliant", []
    return None, fails


def main():
    fixtures_dir = Path(__file__).parent / "fixtures"
    if not fixtures_dir.is_dir():
        print(f"no fixtures directory at {fixtures_dir}", file=sys.stderr)
        return 1
    files = sorted(fixtures_dir.glob("*.json"))
    if not files:
        print(f"no fixtures found in {fixtures_dir}", file=sys.stderr)
        return 1

    print("SPUR Telemetry Profile - accreditation fixture suite\n")
    passed = failed = 0
    for path in files:
        try:
            doc = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            print(f"FAIL  {path.name}\n      invalid JSON: {exc}\n")
            failed += 1
            continue
        if "_test_expected_tier" not in doc:
            print(f"FAIL  {path.name}\n      fixture missing '_test_expected_tier'\n")
            failed += 1
            continue
        expected = doc["_test_expected_tier"]
        if expected is not None and expected not in VALID_TIERS:
            print(
                f"FAIL  {path.name}\n"
                f"      invalid '_test_expected_tier': {expected!r}\n"
            )
            failed += 1
            continue
        description = doc.get("_test_description", "")
        assessed, reasons = assess(doc)
        if assessed == expected:
            passed += 1
            print(f"PASS  {path.name}")
            print(f"      {expected or 'no tier'} - {description}\n")
        else:
            failed += 1
            print(f"FAIL  {path.name}")
            print(
                f"      expected {expected or 'no tier'}, "
                f"assessed {assessed or 'no tier'}"
            )
            if description:
                print(f"      {description}")
            if reasons:
                print(f"      blocked by:")
                for reason in reasons:
                    print(f"        - {reason}")
            elif expected is None and assessed is not None:
                print(f"      expected no tier, but the document qualifies for {assessed}")
            print()

    total = passed + failed
    print(f"{total} fixtures: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
