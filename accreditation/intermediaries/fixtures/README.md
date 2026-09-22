# Intermediary assessment fixtures

> **Consultation draft; not adopted.** [Status and review](../../../CONSULTATION.md).

Run from the repository root:

```sh
python3 accreditation/validate.py
python3 accreditation/intermediaries/fixtures/validate.py
```

Python 3.9 or later; standard library only. No installation, sibling checkout,
network access or credentials are needed. The runner resolves its default
vectors relative to its own path and writes no files. An optional directory
argument selects a different vector set. Exit 0 means all expected findings
matched exactly. A missing or empty suite, malformed case, wrong finding, or
absence of a positive or negative class fails the run.

## Layout and coverage

Each file in `vectors/` contains `case_type`, `description`, explicit
`expected_errors` and the observations needed by that check. An empty error
list means pass; a negative vector must produce exactly its listed error set.
These are assessment wrappers, not top-level Content Telemetry documents.

| Class | Positive vectors | Negative vectors |
|---|---|---|
| `configuration` | Unchanged binding JSON, including unknown nested fields | Missing level, weakened coverage, dropped extension and integer changed to boolean |
| `carriage` | Two publishers with distinct conditions and per-result delivery identifiers | Missing requirement, grant, terms or delivery ID; wrong publisher condition; rewritten profile; stripped extension; reused delivery ID |
| `reconciliation` | Paired index and agent observations; ID-only and URL-only content; stable ID across URL aliases; identical telemetry retry; repeated content with a fresh delivery ID | Missing or unexpected observations; wrong correlation, content, source role, grant, terms, supplier or reporting agent; duplicate logical observation; conflicting retry; shared event ID |
| `publisher_access` | Publisher-approved hosted export preserves both observations; explicit destination takes precedence; reordered export | No publisher agreement, bespoke-only export, default overriding publisher choice, missing agent observation, dropped extension, another publisher's event |

The independent `declarations` are the expected licence conditions. `results`
are captured normalised API outputs. Their ordering identifies the test result;
the runner compares every supplied condition against its publisher declaration.
`source` and `forwarded` test JSON-value preservation separately. Unknown fields
are preserved, not interpreted. These checks do not certify satisfaction of
unknown conditions or turn `selected` coverage into profile compliance.

`deliveries` are assessor-observed supplies. `index_reports` and `agent_reports`
wrap standalone telemetry documents under `document`. Index and agent event
`id` values differ; identical JSON-value retries with the same emitter/event ID
are one logical observation. Distinct event IDs for the same supplied item are
a duplicate finding. Grant and terms references must match the supply record.
The suite models one supplying service and a configured test-agent identity;
authenticated identity binding is independently assessed live.

Publisher-access cases compare `expected_documents` with normalised
`exported_documents` or `forwarded_documents` after required privacy filtering.
These are complete publisher views collected across all pages; order can differ.
The expected view is independently established by the assessor. Agreement and
self-service flags represent live observations, not claims accepted from a
candidate. The fixtures do not test actual account access, pagination, retention,
timing or permission enforcement; the consumer procedure supplies those checks.
Destination and access keys are assessment wrappers, not new core/binding fields.

## Shared pilot interface

The normalised result matches the agent requirements's `result_record`:

```json
{
  "supplying_intermediary": "https://grounding.example/.well-known/content-telemetry.json",
  "delivery_id": "00000000-0000-4000-8000-000000000065",
  "content_id": "a:article:1",
  "license_ref": "licence:a:2026:1",
  "terms_ref": "https://publisher_a.example/terms/v1",
  "profile": "https://contenttelemetry.org/profiles/spur",
  "endpoint": "https://publisher_a.example/licence-events",
  "reporting": { "conformance_level": "retrieval" }
}
```

`reporting` is the existing binding JSON, unchanged. `profile` and `endpoint`
are enclosing licence-declaration values, not new configuration fields.
`reporting_agent_id` in the fixtures is an assessor's authenticated recipient
mapping, not a proposed API field. `content_url` and `content_id` retain their
standard names and source identity. The binding profile URI is reserved for
registration, as documented in `bindings/README.md`.

For the local pilot, both observers' event `data` contains:

```json
{
  "spur_agent_draft": {
    "supplying_intermediary": "https://grounding.example/.well-known/content-telemetry.json",
    "delivery_id": "00000000-0000-4000-8000-000000000065"
  }
}
```

This adopts the agent draft's explicit placeholder; it is not an approved core
hook. Standard section 11.1 permits metadata in `data`. Each pilot adapter and
consumer must explicitly preserve and interpret this extension. Tolerance of
unknown fields alone does not establish that capability. The agent draft
additionally tests preservation of these fields on grounding and citation, including its cache
requirements. The intermediary suite concerns supply and retrieval joins.

The supplying service allocates a fresh opaque `delivery_id` per supplied
item occurrence. UUIDs are used here, but the pilot identifier is not required
to be a UUID. It is distinct from a request ID, `license_ref`, event `id` and
earlier publisher acquisition identifier. `content_telemetry_id` retains its
existing HTTP request-correlation meaning; these API vectors do not overload
it. No HTTP correlation field is required for an API-only local delivery join.

## Limits

The suite checks selected binding structure and deterministic carriage and
reconciliation rules. It is not a JSON Schema implementation. Manifest URI
validation, standard application-layer conformance, cryptographic identity,
acquisition controls, live capability negotiation, lifecycle reporting,
publisher resolution and isolation, cadence, delivery acknowledgements,
production completeness and incident response require the separate checks in
`../ASSESSMENT.md`. Synthetic captures do not prove that a provider operated
the tested behaviour. No outcome is labelled an accreditation award.
