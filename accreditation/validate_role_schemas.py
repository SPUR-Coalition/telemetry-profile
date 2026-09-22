#!/usr/bin/env python3
"""Validate wire artefacts in positive role fixtures against the pinned standard.

Requires the same jsonschema[format-nongpl] environment as validate_schemas.py.
Negative role vectors pin assessment findings in their dependency-free runners;
they are not uniformly invalid core documents and are not assessed here.
Event fragments receive a synthetic standalone envelope for structural checks.
This does not establish cumulative Citation capability or operational behaviour.

Usage: python3 -B accreditation/validate_role_schemas.py /path/to/telemetry
"""

import json
import sys
from pathlib import Path


def artefacts(root):
    for path in sorted((root / "agents" / "fixtures").glob("*.json")):
        for case in json.loads(path.read_text()):
            if case["expected_findings"]:
                continue
            name = f"{path.name}:{case['name']}"
            for field in ("report", "manifest"):
                if field in case:
                    yield name + ":" + field, field, case[field]
            if "result_record" in case:
                yield name + ":reporting", "configuration", case["result_record"]["reporting"]
                yield name + ":forwarded", "configuration", case["agent_condition_record"]
                for number, event in enumerate([case["index_event"]] + case["agent_events"]):
                    yield name + f":event[{number}]", "report", {
                        "document_type": "event",
                        "schema_version": "1.0",
                        "session_id": "770e8400-e29b-41d4-a716-000000000999",
                        "agent_id": "agent:test",
                        "started_at": "2026-09-15T10:00:00Z",
                        "event": event,
                    }
    for path in sorted((root / "intermediaries" / "fixtures" / "vectors").glob("*.json")):
        case = json.loads(path.read_text())
        if case["expected_errors"]:
            continue
        if case["case_type"] == "configuration":
            for field in ("source", "forwarded"):
                yield path.name + ":" + field, "configuration", case[field]
        if case["case_type"] == "carriage":
            for field in ("declarations", "results"):
                for number, result in enumerate(case[field]):
                    yield path.name + f":{field}[{number}]", "configuration", result["reporting"]
        if case["case_type"] == "publisher_access":
            for field in ("expected_documents", "exported_documents", "forwarded_documents"):
                for number, document in enumerate(case[field]):
                    yield path.name + f":{field}[{number}]", "report", document
        for role in ("index", "agent"):
            for number, report in enumerate(case.get(role + "_reports", [])):
                yield path.name + f":{role}[{number}]", "report", report["document"]


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    standard = Path(sys.argv[1]).resolve()
    if not (standard / "tests" / "validate.py").is_file():
        print("no standard reference validator at " + str(standard), file=sys.stderr)
        return 2
    sys.path.insert(0, str(standard / "tests"))
    import validate as std
    from jsonschema import Draft202012Validator

    schema, event_schema, batch_schema, session_validator, manifest_validator, registry = std.load_schema(
        standard / "telemetry-session.json"
    )
    root = Path(__file__).parent
    binding = Draft202012Validator(
        json.loads((root.parent / "bindings" / "reporting-config.schema.json").read_text()),
        format_checker=std.FORMAT_CHECKER,
    )
    failed = count = 0
    for name, kind, document in artefacts(root):
        count += 1
        application_errors = []
        if kind == "configuration":
            schema_errors = list(binding.iter_errors(document))
        elif kind == "manifest":
            schema_errors = list(manifest_validator.iter_errors(document))
            application_errors = std.check_manifest_application_layer(document)
        else:
            if std.is_standalone_event(document):
                schema_errors = std.validate_standalone_event(document, schema, event_schema, registry)
            elif std.is_event_batch(document):
                schema_errors = std.validate_event_batch(document, schema, batch_schema, registry)
            else:
                schema_errors = list(session_validator.iter_errors(document))
            application_errors = std.check_application_layer(document)
        errors = [f"{e.json_path}: {e.message}" for e in schema_errors] + application_errors
        if errors:
            failed += 1
            print(f"FAIL {name}: {'; '.join(errors)}")
    if not count:
        print("FAIL no positive wire artefacts found")
        return 1
    print(f"{count} positive wire artefacts; {failed} failures")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
