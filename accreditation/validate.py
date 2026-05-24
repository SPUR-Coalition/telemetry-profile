#!/usr/bin/env python3
"""Accreditation tier assessment for the SPUR Telemetry Profile.

Determines the highest profile tier a SPUR Telemetry document reaches, by
checking the conformance-level requirements (standard, section 5.7) and the
privacy floor (PROFILE.md section 6). Runs the fixture suite in fixtures/ and
checks each fixture's assessed tier against its declared `_test_expected_tier`.

No external dependencies. Validating a document against the JSON Schema is the
standard repository's test suite; this runner assumes fixtures are well-formed
SPUR Telemetry documents and assesses which tier they reach.

Usage:
    python3 validate.py
"""

import json
import sys
from pathlib import Path

PRIVACY_RANK = {"minimal": 0, "intent": 1, "summary": 2, "full": 3}
TURN_EVENTS = {"turn_started", "turn_completed"}
CONTENT_EVENTS = {
    "content_retrieved",
    "content_grounded",
    "content_cited",
    "content_displayed",
    "content_engaged",
}
TEXT_FIELDS = {"query_text", "response_text"}
INTENT_ONLY_FIELDS = {
    "query_intent",
    "topics",
    "response_type",
    "response_mode",
    "model_id",
    "ad_rendered",
}
VALID_TIERS = ("compliant", "preferred", "strategic")


def events(doc):
    """Yield the document's events, whether it is a session or standalone event."""
    if doc.get("document_type") == "event":
        event = doc.get("event")
        return [event] if event else []
    return doc.get("events", []) or []


def check_retrieval(doc):
    """Retrieval conformance — standard section 5.7.1."""
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


def check_grounding(doc):
    """Grounding conformance — standard section 5.7.2. Cumulative on Retrieval."""
    fails = check_retrieval(doc)
    if doc.get("document_type") == "event":
        fails.append(
            "standalone event document carries no session — "
            "Grounding conformance needs a session"
        )
        return fails
    for field in ("schema_version", "session_id", "agent_id", "started_at"):
        if not doc.get(field):
            fails.append(f"session missing required field '{field}'")
    evs = events(doc)
    grounded = [e for e in evs if e.get("type") == "content_grounded"]
    if not grounded:
        fails.append("no content_grounded event")
    for i, event in enumerate(grounded):
        if "scope" not in (event.get("data") or {}):
            fails.append(f"content_grounded[{i}]: missing 'data.scope'")
    if not any(e.get("type") == "turn_started" for e in evs):
        fails.append("no turn_started event")
    if not any(e.get("type") == "turn_completed" for e in evs):
        fails.append("no turn_completed event")
    for i, event in enumerate(evs):
        if event.get("type") in TURN_EVENTS and "privacy_level" not in (
            event.get("turn") or {}
        ):
            fails.append(f"event[{i}] {event['type']}: turn missing 'privacy_level'")
    return fails


def check_attribution(doc):
    """Attribution conformance — standard section 5.7.3. Cumulative on Grounding."""
    fails = check_grounding(doc)
    evs = events(doc)
    cited = [e for e in evs if e.get("type") == "content_cited"]
    if not cited:
        fails.append("no content_cited event")
    for i, event in enumerate(cited):
        if "citation_type" not in (event.get("data") or {}):
            fails.append(f"content_cited[{i}]: missing 'data.citation_type'")
    for i, event in enumerate(evs):
        if event.get("type") not in TURN_EVENTS:
            continue
        turn = event.get("turn") or {}
        level = turn.get("privacy_level")
        rank = PRIVACY_RANK.get(level, -1)
        present = set(turn)
        if rank <= PRIVACY_RANK["intent"]:
            for field in sorted(TEXT_FIELDS & present):
                fails.append(
                    f"event[{i}] turn: '{field}' not permitted at "
                    f"privacy_level '{level}'"
                )
        if rank <= PRIVACY_RANK["minimal"]:
            for field in sorted(INTENT_ONLY_FIELDS & present):
                fails.append(
                    f"event[{i}] turn: '{field}' not permitted at "
                    f"privacy_level '{level}'"
                )
    return fails


def check_privacy_floor(doc, floor):
    """Privacy floor — PROFILE.md section 6."""
    fails = []
    floor_rank = PRIVACY_RANK[floor]
    for i, event in enumerate(events(doc)):
        if event.get("type") not in TURN_EVENTS:
            continue
        level = (event.get("turn") or {}).get("privacy_level")
        if PRIVACY_RANK.get(level, -1) < floor_rank:
            fails.append(
                f"event[{i}] {event['type']}: privacy_level '{level}' "
                f"is below the '{floor}' floor"
            )
    return fails


def assess(doc):
    """Return (tier or None, {tier: [blocking reasons]}) for a document."""
    reasons = {
        "strategic": check_attribution(doc) + check_privacy_floor(doc, "intent"),
        "preferred": check_grounding(doc) + check_privacy_floor(doc, "intent"),
        "compliant": check_retrieval(doc),
    }
    for tier in ("strategic", "preferred", "compliant"):
        if not reasons[tier]:
            return tier, reasons
    return None, reasons


def main():
    fixtures_dir = Path(__file__).parent / "fixtures"
    if not fixtures_dir.is_dir():
        print(f"no fixtures directory at {fixtures_dir}", file=sys.stderr)
        return 1
    files = sorted(fixtures_dir.glob("*.json"))
    if not files:
        print(f"no fixtures found in {fixtures_dir}", file=sys.stderr)
        return 1

    print("SPUR Telemetry Profile — accreditation fixture suite\n")
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
            print(f"      {expected or 'no tier'} — {description}\n")
        else:
            failed += 1
            print(f"FAIL  {path.name}")
            print(
                f"      expected {expected or 'no tier'}, "
                f"assessed {assessed or 'no tier'}"
            )
            if description:
                print(f"      {description}")
            blocking = reasons.get(expected) if expected else None
            if blocking:
                print(f"      {expected} blocked by:")
                for reason in blocking:
                    print(f"        - {reason}")
            elif expected is None and assessed is not None:
                print(f"      expected no tier, but the document qualifies for {assessed}")
            print()

    total = passed + failed
    print(f"{total} fixtures: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
