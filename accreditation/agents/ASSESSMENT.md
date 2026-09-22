# Independent agent assessment

> **Consultation draft; not adopted.** [Status and review](../../CONSULTATION.md).

**Status:** Consultation draft, 15 September 2026. Procedure for REQUIREMENTS.md.

This is the candidate award procedure. For collaborative development use the
[first PoC](../../CONSULTATION.md#start-with-one-reporting-path), selecting only
the checks needed to answer its question. PoC gaps do not prevent participation.

## 1. Decision and evidence

The assessor MUST be independent of the implementer and its implementation team.
The public record MUST disclose the assessor, commissioning party, payment
relationship, relevant conflicts and how those conflicts were managed. The
implementer MAY supply documentation and attestations but MUST NOT decide
its own result. An unresolved conflict prevents an independent award.

Use `pass`, `fail` and `not_tested` per requirement. An award requires a pass for
every applicable requirement. Record optional lifecycle features and negotiated
exceptions separately. An absent required capability is a failure; unavailable
evidence is `not_tested`. Both block an award.

The fixture runner tests assessment rules over synthetic records. Signature
verification, live tests, inspection and attestation are assessed separately
under PROFILE.md section 6.

## 2. Requirement map

| Requirement | Reproducible checks | Live verification and inspection |
|---|---|---|
| A1 request identity | Preserve verifier input/output and negative signature vectors | Verify each captured HTTP request, directory retrieval, service mapping, rotation, expired and altered signatures, replay rejection under the declared policy, redirect re-signing and non-HTTP authentication |
| A2 telemetry identity | Compare manifest, `agent_id` and `manifest_ref` with the signed-request identity map | Prove domain/key control and pin the deployed build and configuration |
| A3 discovery | Replay licence/configuration snapshots and compare references; test unknown material demands and conflicts | Observe discovery before acquisition, manifest-only limitations, result-level conditions and cache reference retention |
| A4 refusal | Refusal vectors distinguish unauthorised acquisition/use from publisher-authorised exceptions | Challenge capability and route failures, recovery limits and late conditions; inspect publisher logs, buffered reports and model inputs |
| A5 events | Standard schemas and reference application-layer suite at Citation; inspect privacy, cached grounding and output references | Observe generation inputs and resulting source associations independently of emitter reports |
| A6 correlation | Direct log/report reconciliation and intermediary vectors | Capture requests and per-item supplier deliveries; verify upstream identity is not invented |
| A7 delivery | Compare event/dispatch/receipt traces and preserve repeated-event identity | Run long sessions and recovery; confirm consumer accreditation, publisher access/export, onward route and isolation |
| A8 scope | Coverage vectors compare included paths against an assessor inventory | Exercise every entry point, cache, delegated context and attempted bypass |
| A9 declaration | Match manifest coverage entries to the versioned scope record and terms | Verify effective scope, change control and limitations accompanying the mark |
| A10 assessment | Public evidence index and per-requirement results | Independence review, attestation review and signed decision |

## 3. Record the test environment

Before a run, the assessor MUST record:

- Candidate source or release digest, deployment configuration, host integration,
  signer and directory snapshot, manifest and consumer route.
- An independently obtained path inventory from integration documentation,
  configuration, entry-point inspection and network/process observation. Mark
  each path included, disabled or outside the assessed service, with evidence.
- Frozen reporting terms, licence bindings and reporting configuration, including
  references, effective dates and publisher destinations. A bare core manifest
  is a transport control case, not evidence of a minimum reporting demand.
- Synthetic publisher content, stable content identifiers, independently
  controlled publisher logs, intermediary logs and two publisher endpoints.
- Task scripts, seeds, timestamps, clock error, ordinary latency measurements,
  an observation window and a deadline for clearing retry queues. Set numerical
  budgets before testing; they are test-environment bounds, not a new universal
  definition of real time. Classify delayed dispatch separately from loss.

The assessor MUST retain raw captures and derived records with digests and a
transformation log. No emitter-provided success flag substitutes for an assessor
observation. Operational tests MUST use synthetic questions and content suitable
for public release. Private keys, user transcripts and production credentials
MUST NOT enter the public bundle.

## 4. Direct acquisition reconciliation

1. Host at least two publisher sites with manifests and licence bindings requiring
   Citation, complete coverage and real-time delivery. Register both publishers
   with the consumer and choose separate destinations. Check the actual consumer
   assessment record.
2. Drive tasks covering a single fetch, repeated fetches of the same URL, concurrent
   tasks, same-domain and cross-domain redirects, denied requests, retries, unused
   retrieved content, grounding, citations and cached reuse. Exercise all included
   paths and attempt each claimed disabled bypass. Keep tasks running after an
   early retrieval to detect session-end export.
3. Log every request at publisher ingress, before redirects or access gates.
   Capture method, URL, status, timestamp, `Content-Telemetry-ID`, signed components,
   signing identity, response content identity and signature verifier outcome.
   Keep discovery, errors, denial and redirect hops as separate request classes.
4. Establish qualifying content retrievals from response and ingress evidence.
   A discovery request or redirect hop is not automatically another content
   retrieval. A lost response is investigated with client transport evidence;
   it MUST NOT be silently removed to make counts match. All requests remain in
   the evidence bundle. An unresolved occurrence boundary blocks that test.
5. Capture raw arrivals at the consumer and each publisher destination. Match
   agent retrievals to qualifying publisher records on `content_telemetry_id`
   plus `content_url`, or an assessor-verified `content_id` mapping where a
   canonical URL or redirect differs (standard section 7.2). Check publisher,
   timestamp within the declared tolerance, signing identity and terms/licence
   references. Never infer identity from the correlation UUID alone.
6. Report missing expected retrievals, extra agent retrievals and mismatches
   separately. Distinct requests for the same content remain distinct. Origin
   and agent observations are corroborating records, not duplicates to delete
   before comparison. Delivery retries may be de-duplicated only with stable
   event identity and identical payload evidence; divergent duplicates are findings.
7. Measure dispatch delay, consumer receipt and onward publisher receipt per
   event. An event arriving after the deadline is a late-delivery finding even
   if it subsequently clears a missing-event finding. Test recovery without
   discarding the original failure. Reconcile separate runs after remediation.

The local reconciliation vectors use successful, direct, non-redirected
acquisitions and already-normalised event arrivals. They require one agent retrieval for each qualifying acquisition. This model
MUST NOT count every HTTP hop as a separate content event.

Publisher logs corroborate retrieval only. To assess grounding, the assessor
MUST inspect the actual generation-context boundary through test instrumentation
or a verifiable host interface. Compare a fetched-but-discarded item, an item
placed in context, session-scoped reuse and cached grounding. Inspect produced
output source associations to assess citation and join `output_id` and event
identifiers. An answer containing a seeded marker does not by itself establish
which content entered the context. If those boundaries cannot be observed,
record A5 as `not_tested`; an acquisition middleware trace is insufficient.

## 5. Refusal and discovery challenges

Use the same task against supported and unsupported conditions. Test a missing
required capability, unknown material condition, inaccessible required reference,
conflicting terms, incompatible privacy configuration and unavailable consumer.
Without a publisher-authorised alternative, A4 requires refusal before acquisition. Verify no
qualifying publisher acquisition and no grounding or citation of the refused
item, and retain a refusal record naming the condition and failed capability.
A user-facing explanation SHOULD identify the reporting failure without exposing
credentials or unrelated publisher information.

Also deliver the condition with the bytes through a test intermediary. Verify
quarantine before context entry, no cache reuse, the recorded refusal and a
retrieval event for the bytes already received. Do not accept a report that
rewrites this into a pre-acquisition refusal.

Repeat with publisher terms explicitly permitting acquire-and-record. Check the
authorising reference, exception record and retrieval report; independently
confirm that grounding, citation and reuse remain blocked unless separately
authorised. Repeat without that authorisation to detect invented exceptions.
An exception does not satisfy a missing mandatory reporting capability.

Test a temporary outage with a publisher-agreed recovery window and queue limit.
Verify durable retention, reporting-failure visibility and permitted activity
within those bounds; exceed each bound and verify that new affected acquisitions
stop. Restore service and compare original event IDs at the publisher destination.
No agreement must produce the refusal behaviour above. Record late reports
against the agreed cadence and recovery terms, without claiming on-time delivery.

Use a publisher manifest declaring `telemetry.conformance_level: retrieval` as
a control. It MUST NOT override a licence demanding Citation. A core manifest
with no licence condition MUST NOT be misread as a reporting demand. Where an
experimental manifest condition is used, name its adapter and pin its shape;
it is an explicit pilot interface, not a current standard feature.

## 6. Intermediary path

Use `grounding.example` to return two items from different publishers. Each item
carries publisher content identity, `license_ref`, `terms_ref`, its unchanged
reporting configuration, destination and a distinct delivery identifier. The
assessor controls this result adapter and records its mapping to the supplier's
actual API. An agent API credential does not replace A1's request identity.

Compare three independent records: supplier delivery with its `index` observation,
agent receipt/use with its `agent` retrieval observation, and consumer receipt
plus publisher delivery. The paired observations MUST agree on publisher content,
references and delivery correlation. The agent event MUST name the immediate
supplier. Test absent or wrong supplier, altered configuration, an identifier
reused for two deliveries, swapped per-item identities, and a missing agent report.
Keep the supplier's original acquisition from the publisher separate from its
later delivery to the agent.

Repeat with grounded, cited and cached items. Check preservation of supplier and
original delivery reference and `third_party_sourced` provenance; cached grounding
has no new fetch. Where reconciliation is delegated, inspect the consumer's
underlying records and the intermediary's correlated receipts, exception notices
and response. The intermediary need not receive agent events beyond its authorised
view. Verify each publisher receives only its own events at its chosen destination.
If hosted access is offered, exercise the consumer's access/export and destination
change checks in the [consumer procedure](../README.md#consumer-assessment-and-bootstrap).
A test consumer exercises the interface; only a separately accredited consumer
can satisfy the award's dependency. Record that dependency as `not_tested` if no
such consumer is available.

The [fixture fields](fixtures/README.md) are shared with the intermediary
requirements. The assessor MUST record how each implementation maps its API
onto these experimental fields.

## 7. Evidence profile

The shared [evidence guidance](../README.md#evidence-profile) applies. The
assessor MUST record which mechanisms were used and what each result supports.
Grounding and citation still require the direct observations in section 4.

## 8. Public assessment record

Use the shared [public assessment record](../README.md#public-assessment-record).
For agents, include the scope record/digest, host boundary, request identity,
consumer dependency and the grounding/citation observation method. Publish a
reproducible synthetic reconciliation example; raw operational captures and the
full inspected path inventory may remain private with their limits explained.

Apply A9 and PROFILE.md section 6.3 for material-change review and component
reuse. An award names the configuration and review date. The decision authority
must be able to suspend or withdraw the mark when requirements cease to be met;
its appointment, validity and appeal rules remain open before adoption.
