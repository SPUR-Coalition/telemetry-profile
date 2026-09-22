# Agent accreditation requirements

> **Consultation draft; not adopted.** [Status and review](../../CONSULTATION.md).

**Status:** Consultation draft, 15 September 2026.
**Baseline:** Content Telemetry Profile 0.2 and Content Telemetry Specification 1.0.

Source references: [profile](../../PROFILE.md),
[licence bindings](../../bindings/README.md),
[standard](https://github.com/SPUR-Coalition/telemetry/blob/v1.0/SPECIFICATION.md) and
[evidence profile](https://github.com/SPUR-Coalition/telemetry-evidence-profile/blob/4c4924ebc9c7bf747ab26b84b8b110f437280891/README.md).
The external references are pinned to the versions stated above.

These requirements form part of draft profile section 5.7. RFC 2119 and
RFC 8174 keywords have the meanings given in PROFILE.md.

These are candidate award requirements. Start with the smaller
[PoC contract](../../CONSULTATION.md#start-with-one-reporting-path); it does not
require Citation, Web Bot Auth, an accredited consumer or a full path inventory.
Q2 and Q8 leave the universal Citation and signing minima open for review.

## 1. Terms and scope

The terms in [PROFILE.md section 3](../../PROFILE.md#3-terms-and-definitions)
apply. Each service is assessed in every role it performs.

`source_role` MUST be `agent` on the agent's retrieval observations. It MUST
NOT be changed to `index` to identify a supplier. Grounding and citation are
agent observations under the standard; they do not require this field.

Accreditation assesses delivery and observance of declared reporting conditions.
It MUST NOT decide entitlement, ownership, price or compensation. Access evidence
MUST NOT be treated as proof of grounding. Cryptographic validity MUST NOT be
represented as factual truth, completeness or entitlement.

## 2. Identity

### A1. Request identity

The agent MUST sign every outbound HTTP request that directly acquires content
within the assessed service, including retries and redirected acquisitions.
The agent MUST also identify itself on HTTP acquisitions from intermediaries
using the same mechanism. An API credential MAY accompany the signature; it
MUST NOT replace the assessed request identity. A non-HTTP interface MUST have
an independently verified authenticated identity mapped to the same service.

The reference is [draft-ietf-webbotauth-httpsig-protocol-00](https://datatracker.ietf.org/doc/html/draft-ietf-webbotauth-httpsig-protocol-00),
1 September 2026, work in progress, and [RFC 9421](https://www.rfc-editor.org/rfc/rfc9421).
The draft combines request signing and directory discovery. The assessment MUST
pin its revision and verifier. Later revisions require compatibility review.

The agent MUST publish a key directory and use the draft's `directory` discovery
mode. The directory MUST be reachable over HTTPS at
`/.well-known/http-message-signatures-directory`. Requests MUST carry
`Signature`, `Signature-Input` and dictionary-form `Signature-Agent`; the
signature MUST cover its matching `Signature-Agent` member. Draft section 5.2
specifies the required components and parameters; section 5.5 specifies JWKS
discovery, media type and key selection. The telemetry manifest's `keys` array
MUST NOT substitute for this directory.

For assessment, signatures MUST additionally cover `@method`, `@target-uri`
and `content-telemetry-id` when that header is present. This is an accreditation
constraint supported by the draft's additional-component mechanism. Fresh
signatures MUST be generated when those values change. Directory cache lifetimes,
key rotation and replay handling MUST be disclosed and tested.

A valid signature identifies a signing key and the resolved discovery identity.
It does not establish a legal person or delegated authority. Directory key removal
is subject to cache expiry; the draft defines no revocation mechanism.

### A2. Telemetry identity

The agent MUST publish a standard manifest with `roles: ["agent"]`, or a role
array including `agent`. It MUST declare its `conformance_level`, `coverage`
and outbound consumer `endpoint` in `telemetry`. Reports MUST carry `agent_id`
and `manifest_ref` in their session or delivery envelope. The assessor MUST
verify the mapping between these identifiers, the request-signing identity and
the assessed service version.

## 3. Reporting conditions

### A3. Discovery and preservation

Before acquiring content, the agent MUST resolve applicable reporting conditions
from supported licence bindings and the governing terms. It MUST inspect the
publisher's standard manifest for transport information and any separately
agreed reference to a condition. For intermediary content it MUST process the
condition carried with each result, including results in a multi-item response.
A shared response-level condition is sufficient only when its applicability to
every item is explicit and independently testable.

The reporting configuration is defined in
[reporting-config.schema.json](../../bindings/reporting-config.schema.json).
The agent MUST retain that configuration, including unknown fields, and its
`license_ref`, `terms_ref`, publisher identity and publisher-designated destination.
It MUST preserve `terms_ref` unchanged. Applicable references MUST accompany
retrieval, grounding and citation events, including cached reuse. A change of
terms MUST receive a new reference; discovery records MUST retain the earlier
version and time of receipt.

A core manifest cannot demand reporting. Its `telemetry.conformance_level`
describes its own emitter. Its `telemetry.endpoint` does not direct an agent's
complete sessions to a publisher. A manifest-only reporting demand requires an
agreed extension or licence reference; no such field is standardised today.
The assessor MUST distinguish this draft interface from core conformance.

The agent MUST compare each resolved condition with its capabilities, coverage,
cadence, privacy configuration and consumer route. Unknown material requirements,
unresolvable required references and unresolved conflicts MUST be treated as
unmet. Governing terms take precedence over an emitter's coverage declaration.
The agent MUST NOT silently downgrade a demand to its own supported level.

### A4. Unmet conditions

The agent MUST decline acquisition when it cannot meet an applicable reporting
condition and no publisher-authorised alternative applies. An explicit failure
policy in the governing terms MAY permit acquisition with a recorded exception;
permission to acquire MUST NOT be treated as permission to ground, cite or reuse.
The agent MUST retain the authorising reference, failed obligation, action and
remaining reporting duties. It MUST report retrievals that occur and MUST NOT
describe an unfulfilled obligation as fulfilled. Such an exception does not
waive the candidate's required reporting capabilities or privacy restrictions.
Temporary outages remain subject to the bounded recovery rules below; a general
permission to acquire does not waive the remaining delivery obligations.

Where an unmet condition first arrives with content, the agent MUST quarantine that
content, prevent grounding, citation and cache reuse, and record the unmet
condition before continuing the task, unless an explicit applicable alternative
authorises the use concerned. It MUST report any retrieval that already
occurred; refusal MUST NOT erase that occurrence. Discovery and denied HTTP
requests MUST be retained in the assessment log and classified separately from
successful content retrievals. The refusal record MUST identify the content,
condition reference, time, failed capability and action. It is an assessment
record kept separately from core events.

Temporary delivery failure MAY be handled by durable buffering within an
explicit publisher-agreed recovery policy. That policy MUST bound the outage
duration and queue capacity, specify permitted acquisition/use and state when
activity must stop. Without it, or when its limits are exceeded, the agent MUST
stop new acquisitions requiring that route. Already-observed events MUST be
retained and retried without silently dropping occurrences. The publisher and
assessor MUST be able to see failures, exceptions and recovery. Q3 will settle
the policy details; this draft creates no universal grace period.

## 4. Reporting

### A5. Events and semantics

The assessed agent integration MUST demonstrate Citation conformance, including
its cumulative Retrieval and Grounding requirements. It MUST report every
qualifying retrieval, grounding and citation within the assessed relationship.
Other emitter roles retain the minimum conformance level in PROFILE.md
section 5.1.

A retrieval-only component MUST NOT claim this agent accreditation without an
assessed host integration that observes grounding and citation. Content entering
a generation context MUST be reported as grounding. Retrieval selection or
re-ranking alone MUST NOT be reported as grounding. Cached grounding MUST NOT
create a fictitious new retrieval. Citation MUST represent the standard's source
association in output. Presentation and engagement remain optional; when emitted,
section 5.2 coverage applies to them too.

The agent MUST satisfy the standard's schemas and application-layer rules,
including `data.scope`, citation `id`, `output_id`, `data.citation_type` and
conversation-turn privacy restrictions. Accreditation requires no query text,
intent or topics. A disclosure demand incompatible with the applicable privacy
configuration MUST trigger A4. A licence's `privacy_level` MUST NOT be
interpreted to require every permitted field; core requirements and
restrictions continue to apply.

### A6. Correlation and supplying intermediary

Every direct HTTP content acquisition in an assessed reporting relationship MUST
carry a fresh UUID in `Content-Telemetry-ID`. Its retrieval event MUST carry the
same value in `content_telemetry_id`. Repeat acquisitions MUST use distinct
values. Redirect handling MUST retain a documented chain and re-sign each
request; a chain identifier MAY continue across its hops. Cross-domain content
acquisitions in the assessed relationship MUST remain correlatable. The assessor
MUST distinguish transport hops from qualifying content occurrences.

An agent receiving content through an intermediary MUST name the immediate
supplying service on its retrieval and subsequent grounding and citation events.
It MUST preserve the per-item delivery correlation supplied by that intermediary,
including when the representation is cached. It MUST NOT substitute the supplier's
API URL for the publisher's `content_url` or registered `content_id`. Where known,
intermediary grounding MUST carry `data.provenance: third_party_sourced`.

Core has `content_telemetry_id` for HTTP retrieval correlation and `provenance`
for the grounding path. It has no field naming the supplying intermediary or
specified per-item API delivery identifier. The local pilot uses the explicit
draft extension documented in [fixtures/README.md](fixtures/README.md). The
assessor MUST disclose use of that extension. Standardisation is unresolved;
these fields MUST NOT be advertised as core fields or as proof of the supplier's
upstream acquisition. The intermediary's own `index` event remains separate.

### A7. Delivery

The agent MUST dispatch discrete events as they occur to an accredited telemetry
consumer meeting PROFILE.md section 5.5. It MUST support real-time operation
without waiting for the session to close or for a manual export. Ordinary network
and processing latency are permitted. The assessor MUST inspect dispatch and
receipt timestamps, backlog handling and retries.

The consumer route MUST provide publisher access and delivery under PROFILE.md
section 5.5.3, including publisher-approved hosted access/export where selected.
An authorised consumer MAY reconcile reports for the supplying intermediary
and provide receipts and exception notices sufficient for its reporting duties.
The intermediary need not receive the underlying agent events if it delegates
that function; access to any such events requires publisher authorisation.
The agent MUST verify that this route satisfies the carried condition before
accepting it. A complete multi-publisher session MUST NOT be sent to every
publisher or every supplying intermediary.

A publisher MAY agree an alternative cadence or sampling rule in a specific
commercial agreement, as PROFILE.md sections 5.2 and 5.3 permit. The exception
MUST be disclosed, limited to that relationship and assessed against the agreed
rule. It MUST NOT replace demonstration of complete, real-time operation for
the default path. `selected` and `aggregated` do not satisfy this programme.

## 5. Coverage

### A8. Relationship scope

The assessed relationship MUST identify the service and version, host integration,
entry points, acquisition paths, event types, applicable terms and consumer route.
It MUST include every acquisition path that the assessed service mediates and
all subsequent qualifying uses of that content in the assessed integration,
including cache reuse and delegated generation contexts.

The scope MUST be declared before testing. Whether an occurrence falls within
it MUST be decidable before that occurrence.
It MUST NOT depend on whether reporting succeeded, whether content was cited,
the publisher being popular, an individual task outcome, or an emitter's choice
at emission time. A reporting condition MUST NOT be evaded by sending the same
task through an undeclared path. Disabling instrumentation MUST prevent use of
that path under the accredited service. Its declared scope MUST remain unchanged.

Unrelated host activity outside the integration MAY be excluded only with an
explicit boundary and assessor evidence that the assessed service cannot route
its work through it. If bypass is possible, the path MUST be included and
instrumented, disabled for the assessed configuration, or the assessment fails.
The mark and public record MUST name the integration; they MUST NOT imply
coverage of every action on a host. An integration unable to observe required
grounding or citation cannot pass the candidate A5 assessment; it can still
contribute a bounded retrieval PoC to the decision on Q2. The assessor needs
evidence of the integration boundary, not an inventory of unrelated host work.

### A9. Machine-readable declaration and change control

The agent MUST publish `telemetry.coverage` entries for all required and emitted
optional content event types in its standard manifest. Each entry MUST state
`mode` and a `terms_ref` resolving to the applicable relationship declaration.
The default mode MUST be `complete`. Where relationships differ, the recipient
MUST be able to resolve the applicable declaration from event `terms_ref`;
a broad manifest declaration MUST NOT hide an exception.

The assessment MUST include a versioned machine-readable scope record, linked
from the public assessment record and available with the referenced terms.
It MUST identify included paths, justified exclusions, event types, delivery and
consumer, with an immutable digest and effective date. The JSON shape in the
fixtures is an assessment record separate from the core manifest.

The assessor MUST compare the declaration with an independently obtained path
inventory and test for undisclosed paths.
Changes to paths, host integration, signing identity, terms, consumer or reporting
behaviour MUST be recorded and evaluated under PROFILE.md section 6.3. Material
changes require review of affected requirements before the configuration claims
the mark; routine changes through assessed processes need not repeat all tests.

## 6. Independent assessment

### A10. Decision and public evidence

An assessor independent of the implementer MUST execute [ASSESSMENT.md](ASSESSMENT.md),
record conflicts of interest and publish the results and reproducible evidence.
Self-attestation or a fixture pass alone MUST NOT confer this accreditation.
Every applicable requirement MUST pass; untested requirements MUST remain
`not_tested` and block an award. Confidential operational inspection MAY support
the assessment, but the public record MUST state what was inspected and its
limits. Synthetic evidence MUST make the reconciliation tests reproducible.
