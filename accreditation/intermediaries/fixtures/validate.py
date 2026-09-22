#!/usr/bin/env python3
"""Check local intermediary carriage and reconciliation vectors; no dependencies.

This is an assessment adapter, not a core schema validator or accreditation.
Only fixture envelopes use the draft response fields and event extension.
"""

import json
import sys
from pathlib import Path
from uuid import UUID


def is_uuid(value):
    try:
        return isinstance(value, str) and str(UUID(value)) == value.lower()
    except (ValueError, AttributeError):
        return False


def same_json(left, right):
    # JSON booleans must not compare equal to integers as they do in Python.
    return json.dumps(left, sort_keys=True) == json.dumps(right, sort_keys=True)


def configuration_errors(config):
    """Selected rules from the binding; deliberately not full JSON Schema."""
    if not isinstance(config, dict):
        return {"config.object"}
    errors = set()
    enums = {
        "conformance_level": ("retrieval", "grounding", "citation"),
        "privacy_level": ("full", "summary", "intent", "minimal"),
        "delivery": ("real_time", "batch"),
    }
    for field, values in enums.items():
        if (field == "conformance_level" or field in config) and config.get(field) not in values:
            errors.add("config." + field)
    for field in ("manifest", "content_id_scheme"):
        if field in config and not isinstance(config[field], str):
            errors.add("config." + field)
    if "coverage" in config:
        coverage = config["coverage"]
        if not isinstance(coverage, dict) or any(
            mode not in ("complete", "sampled", "aggregated", "selected")
            for mode in coverage.values()
        ):
            errors.add("config.coverage")
    return errors


def configuration(case):
    errors = configuration_errors(case["source"])
    errors |= configuration_errors(case["forwarded"])
    if not same_json(case["source"], case["forwarded"]):
        errors.add("config.changed")
    return errors


def carriage(case):
    errors = set()
    declarations = case["declarations"]
    results = case["results"]
    if len(results) != len(declarations):
        errors.add("result.count")
    for expected, result in zip(declarations, results):
        for field in ("content_url", "content_id", "license_ref", "terms_ref",
                      "supplying_intermediary", "reporting_agent_id", "profile", "endpoint"):
            if field in expected and result.get(field) != expected[field]:
                errors.add("result." + field)
        if not isinstance(result.get("delivery_id"), str) or not result["delivery_id"]:
            errors.add("result.delivery_id")
        if "reporting" not in result:
            errors.add("result.reporting")
            continue
        errors |= configuration_errors(result["reporting"])
        if not same_json(result["reporting"], expected["reporting"]):
            errors.add("result.reporting_changed")
    ids = [result.get("delivery_id") for result in results]
    if len(ids) != len(set(ids)):
        errors.add("result.reused_correlation")
    return errors


def same_content(left, right):
    if left.get("content_id") and right.get("content_id"):
        return left["content_id"] == right["content_id"]
    return bool(left.get("content_url")) and left.get("content_url") == right.get("content_url")


def reconcile(case):
    errors = set()
    deliveries = case["deliveries"]
    ids = [item.get("delivery_id") for item in deliveries]
    if not deliveries or any(not isinstance(value, str) or not value for value in ids):
        errors.add("delivery.correlation")
    if len(ids) != len(set(ids)):
        errors.add("delivery.reused_correlation")
    for role in ("index", "agent"):
        prefix = role + "."
        reports = []
        seen = {}
        for report in case[role + "_reports"]:
            doc = report["document"]
            event = doc["event"]
            if doc.get("document_type") != "event" or doc.get("schema_version") != "1.0":
                errors.add(prefix + "envelope")
            if event.get("type") != "content_retrieved" or event.get("source_role") != role:
                errors.add(prefix + "role")
            if not is_uuid(event.get("id")):
                errors.add(prefix + "identifier")
            if not event.get("timestamp") or not (event.get("content_url") or event.get("content_id")):
                errors.add(prefix + "baseline")
            identity = (doc.get("manifest_ref"), event.get("id"))
            if identity in seen:
                if not same_json(seen[identity], report):
                    errors.add(prefix + "retry_changed")
                continue
            seen[identity] = report
            reports.append(report)
        matched = set()
        for delivery in deliveries:
            candidates = [
                (number, report) for number, report in enumerate(reports)
                if report["document"]["event"].get("data", {}).get("spur_agent_draft", {}).get("delivery_id") == delivery["delivery_id"]
                and same_content(delivery, report["document"]["event"])
            ]
            if not candidates:
                errors.add(prefix + "missing")
            if len(candidates) > 1:
                errors.add(prefix + "duplicate_observation")
            for number, report in candidates:
                matched.add(number)
                doc, event = report["document"], report["document"]["event"]
                for field in ("license_ref", "terms_ref"):
                    if event.get(field) != delivery[field]:
                        errors.add(prefix + field)
                if role == "index":
                    if doc.get("manifest_ref") != delivery["supplying_intermediary"] or event.get("data", {}).get("spur_agent_draft", {}).get("supplying_intermediary") != delivery["supplying_intermediary"]:
                        errors.add(prefix + "emitter")
                else:
                    if doc.get("agent_id") != delivery["reporting_agent_id"]:
                        errors.add(prefix + "emitter")
                    if event.get("data", {}).get("spur_agent_draft", {}).get("supplying_intermediary") != delivery["supplying_intermediary"]:
                        errors.add(prefix + "supplier")
        if len(matched) != len(reports):
            errors.add(prefix + "unexpected")
    index_ids = {r["document"]["event"].get("id") for r in case["index_reports"]}
    agent_ids = {r["document"]["event"].get("id") for r in case["agent_reports"]}
    if index_ids & agent_ids:
        errors.add("pair.shared_event_id")
    return errors


def publisher_access(case):
    """Compare normalised publisher documents; authentication and timing are live checks."""
    errors = set()
    destination = case.get("publisher_destination") or case["default_destination"]
    if not destination or case["observed_destination"] != destination:
        errors.add("access.destination")
    if case.get("publisher_destination"):
        actual = case["forwarded_documents"]
    else:
        if case.get("publisher_agreed_hosted") is not True:
            errors.add("access.agreement")
        if case.get("self_service") is not True:
            errors.add("access.self_service")
        actual = case["exported_documents"]
    expected = case["expected_documents"]
    # Compare a complete publisher view after declared privacy transformations.
    # Array ordering and JSON key order do not affect portable event identity.
    def records(documents):
        return sorted(json.dumps(doc, sort_keys=True) for doc in documents)
    if not expected or records(actual) != records(expected):
        errors.add("access.records")
    return errors


CHECKS = {"configuration": configuration, "carriage": carriage,
          "reconciliation": reconcile, "publisher_access": publisher_access}


def main():
    folder = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).parent / "vectors"
    if len(sys.argv) > 2:
        print("usage: validate.py [vectors_directory]", file=sys.stderr)
        return 2
    files = sorted(folder.glob("*.json"))
    if not files:
        print("FAIL: no fixtures", file=sys.stderr)
        return 1
    failed = 0
    exercised = set()
    for path in files:
        try:
            case = json.loads(path.read_text(encoding="utf-8"))
            expected = case["expected_errors"]
            if not isinstance(expected, list) or any(not isinstance(e, str) for e in expected):
                raise ValueError("expected_errors must be an explicit string list")
            actual = CHECKS[case["case_type"]](case)
            if actual != set(expected):
                raise ValueError(f"expected {sorted(expected)}, got {sorted(actual)}")
            exercised.add((case["case_type"], bool(expected)))
            print("PASS " + path.name)
        except (ValueError, KeyError, TypeError, AttributeError, OSError) as exc:
            failed += 1
            print(f"FAIL {path.name}: {exc}")
    for kind in CHECKS:
        for negative in (False, True):
            if (kind, negative) not in exercised:
                failed += 1
                print(f"FAIL missing {'negative' if negative else 'positive'} {kind} vector")
    print(f"{len(files)} fixtures; {failed} failures")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
