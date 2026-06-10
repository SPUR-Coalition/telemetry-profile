# Licence-layer bindings

How a content-licensing declaration layer requires Content Telemetry reporting as a licence condition, and points at this profile for the rules.

**Status:** Draft (v0.1). For discussion with the RSL working group.

## Why a binding exists

The Content Telemetry standard is permissive by design: an emitter producing well-formed events at any conformance level conforms (profile, section 4). A content owner's `/.well-known/content-telemetry.json` manifest declares where the owner's events should reach, but it has **no way to demand** a minimum conformance level from agents - "the protocol does not give a manifest a way to demand more" (standard, section 8.5).

A **licence** supplies the enforcement context a bare manifest lacks. A licensing layer that makes reporting a condition of the grant ("report at this level or the licence is unavailable for this activity") gives publishers the one lever the manifest deliberately withholds. That is what this binding is for.

The division of labour:

| Layer | Scope | Carries |
|-------|-------|---------|
| Licensing declaration (e.g. RSL `<reporting>`) | Per-licence | The **demand**: minimum conformance level, privacy floor, cadence |
| `/.well-known/content-telemetry.json` manifest | Per-domain | The **transport of record**: signing keys, claimed domains, endpoint |
| This profile | The rules | What "conforming" means, how it is assessed |

A licence carries only what can legitimately vary per licence. It does not restate the manifest. Where both name an endpoint, the licence value is the publisher-designated destination for events under that licence (profile, section 5.4); the manifest remains the domain-level source of truth for keys and claimed domains.

## Profile URI

A licensing layer references this profile by a stable URI:

```
https://contenttelemetry.org/profiles/spur
```

> This URI is reserved for registration; it identifies the SPUR profile as the rule set a Client must follow. Other communities mint their own profile URIs against the same standard.

## Reporting configuration

The JSON object a licensing layer carries (inline or by reference) is validated by
[`reporting-config.schema.json`](./reporting-config.schema.json). Field names match the
Content Telemetry Specification verbatim, so an implementer reads the keys they already
know with no translation. Only `conformance_level` is required; everything else is optional.

## RSL example

Carried inline in the RSL `<reporting>` element body, wrapped in `<![CDATA[ ... ]]>` to avoid XML escaping:

```xml
<rsl xmlns="https://rslstandard.org/rsl">
  <content url="/">
    <license>
      <permits type="usage">ai-input</permits>

      <reporting type="telemetry"
                 profile="https://contenttelemetry.org/profiles/spur"
                 endpoint="https://telemetry.example.com/v1/events">
        <![CDATA[
        {
          "conformance_level": "grounding",
          "privacy_level": "minimal",
          "manifest": "https://example.com/.well-known/content-telemetry.json"
        }
        ]]>
      </reporting>

    </license>
  </content>
</rsl>
```

## Routing note

A single agent session typically grounds content from many publishers. An agent MUST NOT
fan a complete session document out to each publisher's `endpoint` individually - doing so
exposes one publisher's content URLs to another inside the shared session (standard, section 7.3).
The `endpoint` in a licence is therefore the **publisher-designated destination** events must
*reach* (profile, section 5.4), satisfied for agent telemetry by routing through an accredited
telemetry consumer that resolves ownership and exposes each publisher only its own events -
not necessarily a direct POST target. A licensing layer carries the value; this profile defines
how it is honoured.
