#!/usr/bin/env python3
"""Dependency-free checks of synthetic assessment records, not accreditation."""

import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from uuid import UUID
from urllib.parse import urlsplit

REQUIRED_EVENTS = {"content_retrieved", "content_grounded", "content_cited"}
OPTIONAL_EVENTS = {"content_presented", "content_engaged"}


def uuid(value):
    try:
        return isinstance(value, str) and str(UUID(value)) == value
    except (ValueError, TypeError, AttributeError):
        return False


def https(value):
    if not isinstance(value, str):
        return False
    parsed = urlsplit(value)
    return parsed.scheme == "https" and bool(parsed.hostname) and not parsed.username


def moment(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.utcoffset() is None:
        raise ValueError("timestamp requires timezone")
    return parsed


def reconcile(case):
    """Successful direct acquisitions only; raw redirects/denials stay in live tests."""
    findings = set()
    logs = case["publisher_log"]
    doc = case["report"]
    if not logs:
        findings.add("empty_log")
    if doc.get("schema_version") != "1.0" or not uuid(doc.get("session_id")):
        findings.add("report_envelope")
    expected = {}
    for row in logs:
        correlation = row.get("content_telemetry_id")
        if not uuid(correlation):
            findings.add("log_id")
        if correlation in expected:
            findings.add("duplicate_log")
        expected[correlation] = row
        if row.get("signature_valid") is not True:
            findings.add("signature_unverified")
        if doc.get("agent_id") != row.get("agent_id"):
            findings.add("identity_mismatch")
    seen = Counter()
    for event in doc["events"]:
        if event.get("type") != "content_retrieved":
            continue
        correlation = event.get("content_telemetry_id")
        if not uuid(correlation):
            findings.add("report_id")
        if event.get("source_role") != "agent":
            findings.add("source_role")
        seen[correlation] += 1
        if correlation not in expected:
            findings.add("extra")
            continue
        row = expected[correlation]
        # A shared stable identifier is allowed only with an explicit assessor mapping.
        same_content = event.get("content_url") == row.get("content_url")
        if not same_content:
            same_content = (
                row.get("content_id_verified") is True
                and bool(row.get("content_id"))
                and event.get("content_id") == row["content_id"]
            )
        if not same_content:
            findings.add("content_mismatch")
        for field in ("license_ref", "terms_ref"):
            if event.get(field) != row.get(field):
                findings.add("reference_mismatch")
        if abs((moment(event["timestamp"]) - moment(row["timestamp"])).total_seconds()) > 2:
            findings.add("timestamp_mismatch")
    if set(expected) - set(seen):
        findings.add("missing")
    if any(count != 1 for count in seen.values()):
        findings.add("duplicate_report")
    return findings


def coverage(case):
    findings = set()
    scope = case["scope_record"]
    inventory = case["assessor_inventory"]
    required_keys = {
        "scope_version", "content_scope", "agent_id", "service_version",
        "host_integration", "effective_at", "terms_ref", "included_paths",
        "excluded_paths", "event_types", "consumer", "delivery",
    }
    if set(scope) != required_keys:
        findings.add("scope_shape")
    if any(not isinstance(scope.get(k), str) or not scope[k].strip() for k in (
        "scope_version", "content_scope", "agent_id", "service_version",
        "host_integration", "effective_at", "terms_ref", "consumer", "delivery",
    )):
        findings.add("scope_identity")
    moment(scope["effective_at"])
    if not https(scope["consumer"]) or scope["delivery"] != "real_time":
        findings.add("delivery")
    paths = scope["included_paths"]
    if not paths or len(paths) != len(set(paths)):
        findings.add("included_paths")
    indexed = {row["path_id"]: row for row in inventory}
    if not inventory or len(indexed) != len(inventory):
        findings.add("inventory")
    needed = {row["path_id"] for row in inventory if row["can_route_assessed_work"]}
    if not needed.issubset(set(paths)):
        findings.add("scope_omission")
    if set(paths) - set(indexed):
        findings.add("unknown_path")
    excluded = scope["excluded_paths"]
    excluded_ids = [row["path_id"] for row in excluded]
    if len(excluded_ids) != len(set(excluded_ids)) or set(paths) & set(excluded_ids):
        findings.add("exclusion_conflict")
    if set(paths) | set(excluded_ids) != set(indexed):
        findings.add("inventory_mismatch")
    for row in excluded:
        observed = indexed.get(row["path_id"], {})
        if (not row.get("reason") or not row.get("evidence_ref")
                or observed.get("can_route_assessed_work") is not False
                or row.get("evidence_ref") != observed.get("evidence_ref")):
            findings.add("unjustified_exclusion")
    types = scope["event_types"]
    if (not REQUIRED_EVENTS.issubset(set(types))
            or set(types) - REQUIRED_EVENTS - OPTIONAL_EVENTS
            or len(types) != len(set(types))):
        findings.add("event_types")
    manifest = case["manifest"]
    declared = manifest["telemetry"]["coverage"]
    if ("agent" not in manifest["roles"]
            or manifest["telemetry"].get("conformance_level") != "citation"
            or manifest["telemetry"].get("endpoint") != scope["consumer"]):
        findings.add("manifest_identity")
    if set(declared) != set(types):
        findings.add("coverage_types")
    for item in declared.values():
        if item.get("mode") != "complete":
            findings.add("coverage_mode")
        if item.get("terms_ref") != scope["terms_ref"]:
            findings.add("coverage_terms")
    return findings


def intermediary(case):
    findings = set()
    supplied = case["result_record"]
    config = supplied["reporting"]
    if (not supplied.get("license_ref") or not supplied.get("terms_ref")
            or config.get("conformance_level") != "citation"):
        findings.add("condition_missing")
    if json.dumps(case["agent_condition_record"], sort_keys=True) != json.dumps(config, sort_keys=True):
        findings.add("condition_changed")
    if case["agent_endpoint_record"] != supplied["endpoint"]:
        findings.add("endpoint_changed")
    supplier = supplied["supplying_intermediary"]
    if not https(supplier) or not supplied.get("delivery_id"):
        findings.add("delivery_identity")
    index_event = case["index_event"]
    if index_event.get("source_role") != "index" or index_event.get("type") != "content_retrieved":
        findings.add("index_role")
    agent_events = case["agent_events"]
    if Counter(e.get("type") for e in agent_events) != Counter(REQUIRED_EVENTS):
        findings.add("agent_event_types")
    for event in [index_event] + agent_events:
        ext = event.get("data", {}).get("spur_agent_draft", {})
        if ext.get("supplying_intermediary") != supplier:
            findings.add("supplier_missing_or_wrong")
        if ext.get("delivery_id") != supplied["delivery_id"]:
            findings.add("delivery_mismatch")
        for field in ("content_url", "content_id", "license_ref", "terms_ref"):
            if event.get(field) != supplied.get(field):
                findings.add("item_mismatch")
    for event in agent_events:
        if event["type"] == "content_retrieved" and event.get("source_role") != "agent":
            findings.add("agent_role")
        if (event["type"] == "content_grounded"
                and event["data"].get("provenance") != "third_party_sourced"):
            findings.add("provenance")
    return findings


def refusal(case):
    findings = set()
    record = case["refusal_record"]
    if (not record.get("terms_ref") or not record.get("content_url")
            or not record.get("failed_capability")):
        findings.add("refusal_record")
    moment(record["timestamp"])
    # Authorisation is an independently supplied terms snapshot in these records.
    authorisation = case.get("authorisation", {})
    acquired = case["qualifying_acquisitions"] != 0
    permitted = authorisation.get("acquire_and_record") is True
    if acquired and permitted:
        if (not authorisation.get("terms_ref")
                or record.get("authorisation_ref") != authorisation["terms_ref"]):
            findings.add("exception_reference")
        if record.get("action") != "acquired_recorded":
            findings.add("exception_record")
    else:
        if record.get("action") != "declined":
            findings.add("not_declined")
        if acquired:
            findings.add("acquired_despite_condition")
    if case.get("retrieval_reports", 0) != case["qualifying_acquisitions"]:
        findings.add("retrieval_reporting")
    if ((case["grounded"] or case["cited"] or case.get("cache_reused", False))
            and not (permitted and authorisation.get("allow_use") is True)):
        findings.add("used_despite_condition")
    return findings


CHECKS = {"reconciliation": reconcile, "coverage": coverage,
          "intermediary": intermediary, "refusal": refusal}


def main():
    root = Path(__file__).resolve().parent
    total = failed = 0
    names = set()
    for kind, check in CHECKS.items():
        try:
            cases = json.loads((root / (kind + ".json")).read_text())
            if not isinstance(cases, list) or not cases:
                raise ValueError("expected a non-empty case list")
        except (OSError, ValueError) as exc:
            print(f"FAIL {kind}: {exc}")
            failed += 1
            continue
        outcomes = set()
        for case in cases:
            total += 1
            name = case.get("name", "unnamed") if isinstance(case, dict) else "malformed"
            try:
                if name in names:
                    raise ValueError("duplicate case name")
                names.add(name)
                expected = case["expected_findings"]
                if (not isinstance(expected, list)
                        or any(not isinstance(x, str) for x in expected)
                        or len(expected) != len(set(expected))):
                    raise ValueError("invalid expected_findings")
                outcomes.add(bool(expected))
                actual = check(case)
                if actual != set(expected):
                    raise ValueError(f"expected {sorted(expected)}, got {sorted(actual)}")
                print(f"PASS {name}: {', '.join(sorted(actual)) or 'no findings'}")
            except (KeyError, TypeError, ValueError, AttributeError) as exc:
                failed += 1
                print(f"FAIL {name}: {exc}")
        if outcomes != {False, True}:
            failed += 1
            print(f"FAIL {kind}: requires positive and negative vectors")
    print(f"{total} vectors; {failed} failures")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
