# Intermediary accreditation requirements

> **Consultation draft; not adopted.** [Status and review](../../CONSULTATION.md).

**Status:** Consultation draft, 15 September 2026.
**Basis:** Content Telemetry Profile 0.2 and Content Telemetry Specification 1.0.

These requirements form part of draft profile section 5.6. RFC 2119 and
RFC 8174 keywords have the meanings given in PROFILE.md.

These are candidate award requirements. The smaller
[PoC contract](../../CONSULTATION.md#start-with-one-reporting-path) starts with
one supply interface and permits existing authenticated test identities and an
unassessed consumer. Supplying an agent does not require the agent's Citation
capability. Consumers and reconciliation services can be shared or outsourced.

## 1. Scope and terms

The terms in [PROFILE.md section 3](../../PROFILE.md#3-terms-and-definitions)
apply. Each service is assessed in every role it performs.

Accreditation MUST NOT decide entitlement, ownership, price or compensation.
Telemetry references and signatures record claims; governing terms determine
permission.

**I-01 — Assessed service.** The intermediary MUST identify the service,
deployment version, acquisition paths, supply interfaces, catalogue and
reporting relationships in its assessment scope. The scope MUST include all
deliveries through those interfaces, including cache hits, snippets, licensed
feeds and delegated supply paths. It MUST NOT exclude deliveries because an
agent failed to report or because reconciliation failed. Material changes
MUST trigger review of the affected requirements.

## 2. Acquisition

**I-02 — Request identity.** The intermediary MUST identify its service on
each outbound acquisition request. For HTTP acquisition it MUST sign its
requests and publish discoverable verification keys using the pinned
[Web Bot Auth protocol draft, revision 00](https://www.ietf.org/archive/id/draft-ietf-webbotauth-httpsig-protocol-00.html),
including its key directory mechanism. The reference is an Internet-Draft.
The intermediary MUST retain the service identifier and verification result
needed to assess test requests. A signature authenticates the covered message
to a published key; it does not establish permission or the operator's legal
identity. For a non-HTTP feed, the intermediary MUST document the authenticated
service identity and retain receipt records.

**I-03 — Publisher controls.** The intermediary MUST apply
[`robots.txt` under RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html)
to crawling, including matching, caching, redirects and error handling. It
MUST record the AI-use preferences, licence terms and reporting demands
declared for each acquisition. It MUST publish the preference formats and
versions it supports, their discovery points and the precedence rules it
applies. A recognised prohibition MUST prevent the prohibited acquisition or
use. An unknown, conflicting or unresolved declaration MUST NOT be treated
as permission. The intermediary MUST defer the affected activity until it
can apply the publisher's documented instructions. A separately supplied
licence for an API or feed MUST be assessed for that path; it MUST NOT be
treated as a blanket override of a crawling restriction.

The supported formats, discovery points and precedence must be agreed for
each PoC. Q8 must resolve the required set before programme adoption; this
draft does not require discovery or interpretation of every possible format.
Failure to understand a material declaration on a supported path still requires
deferral, not an inference of permission.

**I-04 — Decision records.** Each acquisition MUST be traceable to the
request or feed receipt, service identity, content identifier, acquisition
time, control discovery locations, discovery results and declaration versions.
The record MUST retain the declaration or a digest with an assessor-accessible
snapshot, its effective period, `license_ref`, `terms_ref`, reporting
configuration and the decision taken. An absent declaration MUST be
distinguished from a failed lookup. The intermediary MUST retain refusals and
the governing instruction for any resolved conflict. Terms changes MUST use
a new `terms_ref`; historic references MUST remain resolvable.

The intermediary MUST disclose its refresh and retention rules to the
assessor. Inspection MUST cover refreshed controls, cached content and
withdrawn or changed supply conditions. The assessor checks the records
against controlled publisher declarations and actual requests.

## 3. Reporting conditions in supplied results

**I-05 — Reporting condition.** The intermediary MUST let a publisher name
reporting as a condition of supply through the licence-layer binding in
`bindings/`. It MUST resolve the condition before supplying affected content.
It MUST retain the applicable `license_ref`, `terms_ref`, reporting
configuration, profile reference and publisher-designated endpoint. A
licence-specific endpoint takes precedence for events under that licence, as
specified by the binding; the manifest remains the source for domain claims
and telemetry keys.

A publisher manifest MAY supply discovery and endpoint information. The
intermediary MUST NOT interpret `telemetry.conformance_level` or
`telemetry.coverage` in that manifest as a demand on agents: those fields
describe its own emitter. Standard 1.0 has no manifest reporting-demand hook.
A manifest-only condition therefore needs a new agreed field or an
external licence binding. Until one is available, the intermediary MUST
record the unresolved condition and MUST NOT supply content subject to it.

**I-06 — Conditions on each result.** Each supplied content result MUST carry its
content identifier, applicable `license_ref`, `terms_ref` and reporting
condition, inline or through a resolvable versioned reference. The condition
MUST be available before the agent accepts content subject to it. An interface
that sends metadata with the content MUST disclose the condition during
relationship setup or a metadata-only exchange before that first supply.
Each later result MUST remain independently attributable to its condition.

The intermediary MUST preserve the reporting configuration as a JSON value,
including unknown fields, without weakening, dropping or renaming fields.
Serialisation whitespace and object key order MAY change. If the declaration
is signed, the intermediary MUST also preserve the signed representation or
its original retrievable reference. The enclosing profile reference and
endpoint MUST be preserved separately from the binding's JSON configuration. A multi-publisher response MUST associate each result with its
own condition. A single response-wide condition is insufficient where the
results have different terms. Cache hits and transformed excerpts MUST retain
the applicable source condition and resolvable source identifier.

Absence of `license_ref` MUST NOT be presented as absence of governing terms.
An intermediary MUST NOT invent a licence reference for unlicensed content.
It MUST explicitly record absence in its supply metadata and acquisition
record. Content supplied under a licence requiring reporting MUST carry both
references, even when both resolve to the same document.

**I-07 — Checks before supply.** Before supplying content subject
to reporting, the intermediary MUST authenticate the receiving service,
associate it with its reporting identity and establish a route through an
accredited consumer capable of meeting the condition. It MUST check the
agent's advertised conformance level, declared coverage and agreed reporting
configuration. It MUST decline affected supply when it knows the condition
cannot be met and no explicit publisher-authorised alternative applies. Apply
the failure-policy and bounded-recovery rules in [A4](../agents/REQUIREMENTS.md#a4-unmet-conditions) to supply
as well as acquisition, retaining the authorisation and permitted actions.
A changed condition MUST be recorded and passed to the agent.

An unknown configuration field MUST be preserved. If its meaning is needed
to decide whether reporting can be honoured, supply MUST wait until that
meaning is established. `aggregated` and `selected` coverage do not satisfy
the profile, even though the binding schema can represent them. `sampled`
coverage requires a publisher agreement and a stated sampling rule. Real-time
delivery and `complete` coverage are the defaults.

### 3.1 Existing fields and missing API support

| Information | Existing field or format | Limit for intermediary supply |
|---|---|---|
| Reporting demand | Licence declaration carrying `reporting-config.schema.json` | Draft binding; not a core content-response format |
| Profile and destination | Enclosing licence declaration; manifest `telemetry.endpoint` | Agent sends to its configured accredited consumer, which honours the publisher destination |
| Grant and terms | Event `license_ref` and `terms_ref` | Existing event fields; standard does not define their placement in a retrieval API result |
| Content identity | Event `content_url` and/or `content_id` | API must carry a resolvable source identifier; identifier ownership is verified separately |
| Correlation | Event `content_telemetry_id`; HTTP request `Content-Telemetry-ID` | Per-result API delivery identity is not specified; the local pilot uses a separate `delivery_id` |
| Supplying service | No dedicated core event field | Requires an agreed field; event `manifest_ref` identifies the emitter, not its supplier |
| Manifest-only reporting demand | None in standard 1.0 | Cannot reuse the emitter's conformance or coverage declaration |

The fixtures use an experimental result format and `data.spur_agent_draft`
extension shared with the agent requirements. The assessment MUST identify
how the implementation maps its API onto these records. The fields and mapping
need agreement before adoption.

## 4. Receiving and delivering agent reports

**I-08 — Consumer route.** The intermediary MUST arrange reporting for its
supplied content through a consumer meeting profile section 5.5. It MAY operate
that consumer or use an accredited provider. It MAY delegate reconciliation
as well as receipt, publisher access and delivery. The delegated service MUST
provide delivery-correlated receipts and exception notices sufficient to identify
missing reports, publisher availability or delivery failures and required remedies.
The intermediary MUST act on those notices and keep the consumer identity,
assessed version, responsibilities and route configuration available for inspection.
It need not receive all agent events or duplicate the delegated reconciliation.
Underlying evidence MUST remain available to the assessor. Event access is limited
to what the publisher authorises under I-09.

The receiving consumer MUST associate reports with the
authenticated reporting agent and the supplying intermediary. The emitter's
identity MUST NOT be overwritten with the supplier's identity. The standard
field naming the intermediary awaits agreement. The pilot uses
`data.spur_agent_draft.supplying_intermediary`, bound to authenticated route
metadata. This is the experimental format described in the fixtures.

**I-09 — Publisher resolution and isolation.** The consumer MUST resolve
each event through verified domain or registered identifier-prefix mappings,
as in standard section 7.3. Conflicting owner resolutions MUST be withheld
from both publishers until resolved by trust policy. Unresolved events MUST
be retained under a documented retention policy and reported as undelivered.
Each publisher MUST receive only its own events. Registration requires
verification of the domain or identifier-prefix claim.

Complete multi-publisher sessions MUST NOT be forwarded to publisher
endpoints. Filtering MUST also prevent session context, extension data or
credentials from exposing another publisher's identifiable telemetry.
Consumer conformance, including all three delivery formats, compatible minor
versions, unknown fields and stripping privacy-violating turn fields, MUST
meet profile section 5.5.1.

**I-10 — Publisher access and delivery.** Both agent reports and the intermediary's
own events MUST be available to the publisher under profile sections 5.2 through
5.5. The intermediary MAY default to its own reporting service with the publisher's
agreement, offering authenticated access and self-service event-level Content
Telemetry export. An explicit publisher destination MUST take precedence. The
publisher MUST be able to choose onward delivery to another service through an
authenticated configuration process. Events must be available as they occur,
unless another cadence is agreed. Aggregate dashboards and bespoke exports only
available by asking the operator are insufficient. The consumer MAY provide all
of these functions on the intermediary's behalf.

The delivery path MUST preserve event identity, content identity,
`content_telemetry_id` where present, the supplying-service and per-item delivery
pair, `license_ref` and `terms_ref`. It MUST identify the original emitter
while applying required privacy filtering. It MUST record dispatch,
acknowledgement, retries and terminal failures. Retry handling MUST preserve
the original event `id` and MUST NOT count a retried report as a new
occurrence. Delivery outages MUST be visible to the publisher and assessor;
buffered events MUST remain available for recovery under the disclosed
retention policy. A reporting outage MUST NOT silently relax a supply
condition.

## 5. The intermediary's own deliveries

**I-11 — Complete index reporting.** The intermediary MUST conform as an
emitter under profile section 5.1. Each qualifying content delivery to an
agent MUST produce a discrete `content_retrieved` event with
`source_role: index`. Coverage MUST be `complete` for those deliveries.
The profile's sampling exception does not apply to this supply record. Agreed
sampling of agent reports is assessed separately.

The intermediary MUST publish `telemetry.coverage.content_retrieved` with
`mode: complete` and a `terms_ref` through which the relationship scope is
disclosed. Standard 1.0 has no structured scope field. The assessment MUST
compare that scope with the actual catalogue and interfaces in I-01,
including filters that may discard reports.

The intermediary MUST report the actual delivery depth where known and MUST
preserve the applicable grant and terms references. A snippet delivery is
not a claim that the agent fetched the full article. Building an index is
outside the standard's inference-time event scope; I-04 acquisition records
do not become inference-time delivery events. Serving cached content to an
agent is a new delivery; retrying its telemetry is not.

**I-12 — Delivery correlation.** Each supplied item occurrence MUST carry an
opaque delivery identifier unique within the supplying service, available
for both index and agent reports. The local pilot names this pair
`supplying_intermediary` and `delivery_id` in each result and in event
`data.spur_agent_draft`. The supplier reference identifies the immediate
service by its manifest URL. The intermediary SHOULD generate UUID values
for `delivery_id`; the pilot treats the value as opaque. It MUST preserve
the pair through the receiving consumer. The index event MUST also have an
emitter-assigned `id`, distinct from the agent event's `id`.

A telemetry retry MUST preserve the event `id` and delivery pair. A new
supply occurrence MUST have a new delivery identifier, including repeated
delivery of the same content. Later agent grounding and citation, including
cached use, retain the original pair under the agent draft's requirements;
they are not new intermediary deliveries.

For a direct HTTP fetch, the existing `Content-Telemetry-ID` request header
and `content_telemetry_id` event field remain the retrieval correlation
mechanism. A multi-result API request UUID MUST NOT substitute for per-item
delivery identity. An earlier publisher acquisition UUID MUST NOT identify
a later delivery from the intermediary's store. The fields used in API
responses, identifier allocation and handling of multiple intermediaries are
not defined by standard section 7.2 and require agreement before adoption.

API reconciliation MUST compare supplying service, delivery identifier and
content identity. Direct HTTP reconciliation compares `content_telemetry_id`
and content identity. Exact `content_url` equality supports the section 7.2
path; a stable `content_id` supports the section 4.5 alternative, including
different URLs for the same content. Contradictory `content_id` values MUST
be reported as findings even when URLs match. Index and agent observations
MUST remain distinguishable after deduplication and be counted as two
observations of one retrieval.

**I-13 — Reconciliation and remedy.** The intermediary MUST ensure reconciliation
of its delivery records, index events, agent retrieval reports and publisher
availability or delivery receipts, directly or through the service in I-08.
Missing, unexpected, conflicting and late reports MUST be recorded
and investigated. A missing agent event MUST NOT be filled with an invented
agent observation. When a reporting condition is no longer supportable, the
intermediary MUST suspend affected supply unless an explicit publisher-authorised
alternative or recovery policy applies under I-07. It MUST retain incident,
authorisation and remedy records, including delegated notices and its response.

A retrieval match corroborates delivery only. It MUST NOT be described as
proof of grounding, citation, complete production coverage or entitlement.
Later lifecycle events are the agent's claims and do not have an independent
index-side counterpart. The assessor MUST assess their delivery separately
where the governing condition requires them.
