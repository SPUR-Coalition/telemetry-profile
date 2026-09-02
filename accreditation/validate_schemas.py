#!/usr/bin/env python3
"""Validate the accreditation fixtures against the standard's v1 schemas.

The profile's own runner (validate.py) assesses fixtures against the Compliant
tier and deliberately assumes they are well-formed Content Telemetry documents.
This script closes that assumption: it validates every fixture against the
standard repository's JSON Schemas and application-layer reference validator,
so a hand-edited fixture cannot drift from the wire format the profile
constrains without CI noticing.

Expectations per fixture:

- ``_test_expected_tier: "compliant"`` - the document must be fully valid:
  no schema errors and no application-layer errors.
- ``_test_expected_tier: null`` - the document is deliberately non-conforming:
  it must be schema-valid (the fixtures demonstrate application-layer
  failures, not malformed JSON documents) and must produce at least one
  application-layer error.

Requires a checkout of the standard repository at the version this profile
constrains (PROFILE.md section 2) and the jsonschema package
(``pip install "jsonschema[format-nongpl]"``).

Usage:
    python3 validate_schemas.py /path/to/telemetry
"""

import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    standard = Path(sys.argv[1]).resolve()
    schema_path = standard / "telemetry-session.json"
    if not schema_path.is_file():
        print(f"no telemetry-session.json under {standard}", file=sys.stderr)
        return 2

    sys.path.insert(0, str(standard / "tests"))
    import validate as std  # the standard's reference validator

    (
        session_schema,
        event_schema,
        batch_schema,
        session_validator,
        _manifest_validator,
        registry,
    ) = std.load_schema(schema_path)

    fixtures = sorted((Path(__file__).parent / "fixtures").glob("*.json"))
    if not fixtures:
        print("no fixtures found", file=sys.stderr)
        return 1

    print("SPUR profile - fixture validation against the standard's schemas\n")
    failed = 0
    for path in fixtures:
        doc = json.loads(path.read_text())
        expected_tier = doc.get("_test_expected_tier")
        if std.is_standalone_event(doc):
            schema_errors = std.validate_standalone_event(
                doc, session_schema, event_schema, registry
            )
        elif std.is_event_batch(doc):
            schema_errors = std.validate_event_batch(
                doc, session_schema, batch_schema, registry
            )
        else:
            schema_errors = list(session_validator.iter_errors(doc))
        app_errors = std.check_application_layer(doc)

        problems = [f"schema: {e.json_path}: {e.message}" for e in schema_errors]
        if expected_tier == "compliant":
            problems += [f"application-layer: {v}" for v in app_errors]
        elif not app_errors:
            problems.append(
                "expected a deliberately non-conforming document, but the "
                "standard's application-layer checks report no error"
            )

        if problems:
            failed += 1
            print(f"FAIL  {path.name}")
            for problem in problems:
                print(f"      {problem}")
            print()
        else:
            print(f"PASS  {path.name}")

    print(f"\n{len(fixtures)} fixtures: {len(fixtures) - failed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
