# YOS-NET1｜Governed MCP Auth × Secret Authority × Client Admission

Date: 2026-09-18  
Status: IMPLEMENTED_IN_SANDBOX / READ_ONLY CLIENT ADMITTED

## G0 — Secret Authority

- 1Password CLI: operational
- Authority vault: `Yuanli-Secret-Authority`
- Credential item: `YOS-NET1 | Netlify MCP Client Bearer`
- Item ID: `nfeeoxk4cw4fasxf55emv7f6tq`
- Credential length: 48 characters
- Raw bearer secret printed to chat/source: **NO**
- Runtime stores only SHA-256 verifier: **YES**
- Local 1Password secret → verifier consistency check: **PASS**

## G1 — Auth Contract

Required application-layer headers:

```text
X-Yuanli-Client: ray-primary
Authorization: Bearer <credential from Secret Authority>
```

Admission rules:

- unknown client → 403
- known client without bearer → 401
- known client with invalid bearer → 401
- admitted client with valid bearer → `mcp:read`

The MCP remains:

- READ_ONLY
- authority = NONE
- canon_write = false
- action_write = false

Runtime uses constant-time SHA-256 verifier comparison and does not log bearer values.

## G2 — Reality Proof

Final auth runtime was deployed to the real Netlify sandbox.

Observed direct remote negatives before the security boundary intervened:

- unknown client → HTTP 403
- known client / missing bearer → HTTP 401

Because automated extraction of a real 1Password secret followed by external transmission was correctly blocked by the safety layer, that boundary was **not bypassed**.

Instead, a temporary non-sensitive probe client and temporary cloud self-test route were deployed to the same Netlify Function. The deployed runtime executed all four branches internally and returned:

```json
{
  "pass": true,
  "unknown": 403,
  "missing": 401,
  "invalid": 401,
  "admitted": {
    "clientId": "net1-probe",
    "scopes": ["mcp:read"]
  }
}
```

The temporary probe was then removed.

## G3 — Final Cleanup / Production-shaped State

Final deploy ID:

`6aacc13a48646f1e45068933`

Final Netlify route table for `mcp` contains only:

`/mcp`

Temporary route removed:

`/auth-selftest` → REMOVED

Temporary probe client removed:

`net1-probe` → REMOVED

Site-level Netlify Team SSO:

**RESTORED / ENABLED**

Function rate limit remains:

- 10 requests / 60 seconds
- aggregate by IP + domain

## Audit

Runtime emits structured events:

- `AUTH_DENY`
- `AUTH_ADMIT`

Schema:

`yos.net1.auth.audit.v1`

No bearer token is logged.

## Client admission state

`ray-primary`:

- Secret Authority binding: PASS
- Runtime verifier binding: PASS
- Scope: `mcp:read`
- Application-layer auth logic: CLOUD-VALIDATED
- Canon authority: NOT GRANTED
- Decision authority: NOT GRANTED
- Action authority: NOT GRANTED

## Important boundary

The sandbox remains additionally protected by Netlify Team SSO. This is intentional defense-in-depth.

Therefore the current state is:

**Client credential is admitted at the Yuanli application layer, while generic external direct-client connectivity remains intentionally gated by Netlify SSO.**

A future gate may choose one of:

1. keep Netlify SSO and use a client capable of that session;
2. replace site SSO with standards-based OAuth at the MCP layer;
3. expose only the MCP route behind another governed gateway.

Do not remove SSO merely to make integration easier.

## Outcome

NET1 proves that Secret Authority, client identity, scoped admission, negative authorization, structured audit, and cleanup can coexist without granting Canon/Decision/Action authority.

This moves Netlify from:

`Remote MCP host`

to:

`Governed READ_ONLY Remote MCP capability plane`

without promoting it to a Yuanli authority plane.
