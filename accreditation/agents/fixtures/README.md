# Agent assessment fixtures

> **Consultation draft; not adopted.** [Status and review](../../../CONSULTATION.md).

Run from the repository root:

```sh
python3 accreditation/validate.py
python3 accreditation/agents/fixtures/run.py
```

Python 3.9 or later; standard library only, no network calls, installations or
sibling checkout required. Paths resolve relative to the runner. Exit 0 means
all expected findings matched exactly, including the negative vectors. These
commands do not write files. The original Retrieval cases retain their historical annotations.

## Evidence format

Each JSON file is a list of independent cases with `name` and
`expected_findings`. An empty finding list is a positive case. Negative cases
name the exact findings, so an unrelated error cannot satisfy a negative test.
Missing files, empty suites, malformed cases and absent positive/negative classes
fail the runner. These wrappers are local assessment records, not core documents.

| File | Evidence and checks |
|---|---|
| `reconciliation.json` | Signed-request verification results in a synthetic publisher log and standard session reports: missing, extra, duplicated or mismatched retrievals, identity, UUID, content, references and time |
| `coverage.json` | Standard manifest coverage plus local scope JSON, compared with an independently supplied path inventory: omitted paths, discretionary conditions, unsupported coverage modes and missing lifecycle coverage |
| `intermediary.json` | Per-item result assessment record, unchanged reporting configuration, paired index/agent retrievals and agent grounding/citation: supplier identity, original content, terms and delivery join |
| `refusal.json` | Known unmet conditions and independent observations: refusal without authorisation; permitted acquisition with an exception reference and retrieval report; separate permission for grounding, citation and cache reuse |

The reconciliation time tolerance is two seconds for synthetic occurrence clocks,
not a definition of real-time delivery. Its publisher log contains qualifying
successful acquisitions only. The live procedure retains and classifies every
HTTP request, including discovery, refusal, lost responses and redirect hops.
`signature_valid` is a stand-in for an independent verifier result; Python does
not verify cryptographic signatures here. The fixture pass does not prove logs
are authentic or complete. Coverage inventory flags likewise represent external
inspection findings; they are not self-attested grounds for accreditation.

Refusal cases use `authorisation` as a normalised, independently supplied terms
snapshot, not a new wire field. `refusal_record` also holds exception actions for
compatibility with the existing wrapper. Its `authorisation_ref` links the action
to the terms permitting acquisition; `allow_use` is separate. Retrieval counts
stand in for captured reports here. Actual authorisation, privacy, durable queues,
recovery limits and eventual publisher receipt are tested live under A4/A7.

## Coverage record

`scope_record` is a local assessment record. `scope_version` versions its shape;
`content_scope`, `agent_id`, `service_version`, `host_integration`, `effective_at`
and `terms_ref` bind the declaration. `included_paths` names the fixed assessed
paths. `excluded_paths` gives `path_id`, `reason` and `evidence_ref` for each
exclusion. `event_types`, `consumer` and `delivery` state the reporting boundary.
The public assessment links to and hashes the immutable record. No new core
manifest field is defined. Existing `telemetry.coverage` entries retain the
standard's `{ "mode": "complete", "terms_ref": "…" }` shape.

The independent inventory states whether each path can route assessed work.
All such paths must be included. A justified excluded host path cannot route that
work. The runner tests the default complete, real-time relationship. Negotiated
sampling or cadence exceptions require a separate, published agreement-specific
suite and live assessment; this runner rejects them rather than certifying an
untested exception. Optional presentation/engagement, when listed, also require
coverage entries. It cannot verify path independence from a declaration alone.

## Intermediary interface pending integration

`result_record` is an assessor's normalised per-item API observation, not a proposed
standard API schema. Existing content and reference fields keep their standard
spelling. `reporting` contains the existing bindings configuration unchanged,
including an unknown test field. `endpoint` is the publisher's destination,
carried separately from that configuration as in the licence binding.

For the local pilot only, event `data` carries a namespaced extension:

```json
{
  "spur_agent_draft": {
    "supplying_intermediary": "https://grounding.example/.well-known/content-telemetry.json",
    "delivery_id": "delivery:0001"
  }
}
```

The supplier reference names the immediate service. The opaque identifier is
unique per item delivery within that service, not a licence, request UUID or
publisher acquisition identifier. Both sides retain the pair. The result adapter
maps it onto the index observation and the agent's receipt, grounding and citation;
cached uses retain the original pair. Events still identify the original publisher
content. `content_telemetry_id` remains the existing HTTP correlation field; a
single API request UUID does not identify every item or later cached delivery.

These extension names are local placeholders; they do not assert an approved
standard hook. Core permits namespaced `data` extensions (section 11.1). A
consumer's obligation to tolerate unknown fields does not guarantee preservation
or interpretation; the pilot consumer must explicitly support this extension.
Both role suites use these field names; their assessment wrappers differ.
The pilot adapter must publish its mapping and demonstrate a round trip.
See the [intermediary fixtures](../../intermediaries/fixtures/README.md).

## Limits

The runner tests reconciliation rules, not full JSON Schema or standard
application-layer conformance. It does not test real-time transport, network
identity, refusal implementation, publisher isolation, late-condition quarantine,
cache use or runtime scope enforcement. ASSESSMENT.md requires these live checks
and the standard's own Citation conformance checks separately. No fixture result
is labelled an accreditation award.
