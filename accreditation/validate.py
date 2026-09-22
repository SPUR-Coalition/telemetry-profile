#!/usr/bin/env python3
"""Retrieval baseline regression fixtures for the SPUR Content Telemetry Profile.

The original fixtures retain their historical ``compliant`` / None labels.
Those labels concern this baseline only. The accreditation-design draft adds
role-specific requirements and independent operational assessment; this runner
neither checks all of them nor awards accreditation.

No external dependencies. Full schema and application-layer conformance is
checked separately against the pinned standard. Usage: python3 validate.py
"""

import json
import sys
from pathlib import Path

CONTENT_EVENTS = {
    "content_retrieved",
    "content_grounded",
    "content_cited",
    "content_presented",
    "content_engaged",
}
LEGACY_EVENT_TYPES = {"content_displayed"}
VALID_TIERS = ("compliant",)


def events(doc):
    """Yield the document's events, whether it is a session or standalone event."""
    if doc.get("document_type") == "event":
        event = doc.get("event")
        return [event] if event else []
    return doc.get("events", []) or []


def check_document(doc):
    """Document-level checks: the v1 wire version and withdrawn event types.

    A v1 consumer rejects documents declaring "0.1" (standard, section 5.7.4),
    and v1 replaces content_displayed with content_presented (standard,
    section 12.1). A document a conforming consumer must reject cannot be
    assessed Compliant.
    """
    fails = []
    version = doc.get("schema_version")
    if not isinstance(version, str) or not version.startswith("1."):
        fails.append(
            f"document: schema_version {version!r} is not a v1 version; "
            "a v1 consumer rejects this document"
        )
    for i, event in enumerate(events(doc)):
        etype = event.get("type")
        if etype in LEGACY_EVENT_TYPES:
            fails.append(
                f"event[{i}]: {etype!r} is a withdrawn v0.1 event type; "
                "v1 replaces content_displayed with content_presented"
            )
    return fails


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
    """Return the historical baseline label and blocking reasons for a document."""
    fails = check_document(doc) + check_retrieval(doc)
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

    print("SPUR Content Telemetry Profile - Retrieval baseline fixtures (not an award)\n")
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
        assessed, reasons = assess(doc)
        expected_label = "Retrieval pass" if expected else "Retrieval failure"
        assessed_label = "Retrieval pass" if assessed else "Retrieval failure"
        if assessed == expected:
            passed += 1
            print(f"PASS  {path.name}")
            print(f"      expected {expected_label}\n")
        else:
            failed += 1
            print(f"FAIL  {path.name}")
            print(
                f"      expected {expected_label}, got {assessed_label}"
            )
            if reasons:
                print(f"      blocked by:")
                for reason in reasons:
                    print(f"        - {reason}")
            elif expected is None and assessed is not None:
                print("      expected the Retrieval check to fail")
            print()

    total = passed + failed
    print(f"{total} fixtures: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
