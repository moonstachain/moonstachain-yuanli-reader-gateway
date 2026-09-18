# YOS-NET0｜Netlify Remote MCP Reality Receipt

Date: 2026-09-18
Status: G0-G3 PASS; G4 evidence/outcome writeback in progress

## Scope
Isolated experiment only. No changes to main, Soul canon, knowledge canon, investment runtime, or health runtime.

## G0 — Authority Admission
- ChatGPT ↔ Netlify authenticated control-plane read: PASS
- Netlify project created: `yuanli-netlify-reality-sandbox`
- Project ID: `cd871f7c-59e5-47db-8f08-f93a5ab681dd`

## G1 — Reality Surface
- Static page deployed to Netlify: PASS
- Production deploy ready: PASS
- Initial deploy ID: `6aacb681ca2d0720d8de2618`
- SSO visitor protection observed externally as HTTP 401: PASS

## G2 — Read-only Endpoint
- Function route `/yuanli-context` deployed: PASS
- Contract: READ_ONLY / authority NONE / no canon write / no action write

## G3 — Standard Remote MCP
- Netlify Function `mcp` deployed at `/mcp`: PASS
- Runtime: Node.js 24
- Stateless Streamable HTTP transport: PASS
- Function-level rate limit: 10 requests / 60 seconds by ip+domain: PASS
- Deploy ID: `6aacb70d5c91ee266faa29d4`

### Protocol proof
A temporary public-access window was opened only for the non-sensitive protocol test and then SSO was restored.

1. `initialize` → HTTP 200
2. `tools/list` → HTTP 200; discovered `get_yuanli_context`
3. `tools/call` → HTTP 200; returned `G3_REMOTE_MCP_OK`

Returned authority boundary:
- mode: READ_ONLY
- authority: NONE
- canon_write: false
- action_write: false

## Safety / governance observations
1. Netlify control-plane rejected direct Agent insertion of a newly generated secret. Treat this as a positive Secret-Plane boundary.
2. Site-level SSO was restored immediately after protocol verification.
3. Public MCP without bearer auth is NOT approved for production; current proof remains behind Netlify SSO.
4. No production Canon, Decision, Action, or private knowledge was exposed.

## Learning
Netlify is validated as a replaceable Yuanli C4 delivery / Reality Sandbox capability:
- web delivery
- serverless function runtime
- Remote MCP host
- deploy/readback surface

It is NOT validated as:
- Canon authority
- Brain authority
- Decision authority
- Secret authority

## Next admission gate
Production-grade Remote MCP requires one of:
- governed bearer/OAuth secret injection through the approved Secret Authority plane; or
- another client-auth mechanism compatible with Yuanli sovereignty and least authority.

Do not promote this experiment to production capability until that auth gate passes.


## G4 — Netlify vs Vercel controlled comparison

### Vercel control object
A separate Vercel project was created only as a control:
- project: `yuanli-vercel-mcp-control`
- final deployment: `dpl_61gkCgW9ecrFerwYZwPZCqurjr8U`
- deployment state: READY
- route: `/api/mcp`
- tool: `get_yuanli_context`

### Vercel learning trail
Two failed build attempts were intentionally preserved as evidence:
1. missing TypeScript build dependencies -> build gate rejected the deploy;
2. current `mcp-handler` 2.x API differs from 1.x examples -> `server.tool` and legacy 3-argument `createMcpHandler` failed type-checking.

After migrating to the current 2.x contract:
- `mcp-handler ^2.1.1`
- `@modelcontextprotocol/server ^2`
- `zod ^4`
- `server.registerTool(...)`
- two-argument/current `createMcpHandler` usage

the deployment reached READY.

### Vercel protocol proof
The Vercel deployment was protected by Vercel Authentication. A temporary expiring share token was used for the test; the project itself was not made public.

1. `initialize` -> HTTP 200
2. `tools/list` -> HTTP 200; discovered `get_yuanli_context`
3. `tools/call` -> HTTP 200; returned `VERCEL_MCP_CONTROL_OK`

### Observed platform differences in this experiment

| Dimension | Netlify | Vercel |
|---|---|---|
| Minimal MCP host | Direct Netlify Function + MCP SDK | Next.js route + `mcp-handler` |
| First successful MCP deploy | 1 code iteration | 3 code iterations including 2 useful build failures |
| Access gate used | Netlify team SSO | Vercel Authentication + expiring share token for test |
| Protocol call | PASS | PASS |
| Function-level rate limit in proof | Native config applied (10/60s by ip+domain) | Not configured in this control |
| Production promotion | Netlify upload deploy used production context, then protected by SSO | Control remained non-production/preview-style protected deployment |
| Framework overhead | Lower for this proof | Higher for this proof |

### G4 outcome
Both platforms are technically viable as replaceable Yuanli Remote MCP / Web Reality delivery planes.

For the narrow use case tested here — **small, stateless, governed Remote MCP endpoints with minimum framework surface** — Netlify produced the simpler path and native function-level rate-limit proof.

Vercel demonstrated stronger first-class MCP ecosystem ergonomics around `mcp-handler`, preview/auth tooling, and official MCP hosting guidance, but the current SDK v2 migration requires version-aware implementation discipline.

This is not a permanent platform winner decision. Route future deployments by capability requirements and measured outcomes.

### Admission state
- Netlify C4 Reality/Delivery capability: VALIDATED_IN_SANDBOX
- Vercel C4 Reality/Delivery capability: VALIDATED_IN_SANDBOX
- Production Remote MCP with governed client auth: NOT YET ADMITTED
- Canon / Brain / Decision / Secret authority: NOT GRANTED
