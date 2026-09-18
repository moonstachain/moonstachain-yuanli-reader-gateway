# YOS-NET1｜Governed MCP Auth Contract

## Authority model

- Human Principal remains the authority owner.
- 1Password `Yuanli-Secret-Authority` is the secret authority.
- Netlify receives no raw client bearer secret in source code.
- Runtime source contains only a one-way SHA-256 verifier.
- MCP tools remain read-only and authority-none.

## Client admission v1

| Client ID | Scope | Secret Authority | Runtime verifier |
|---|---|---|---|
| `ray-primary` | `mcp:read` | 1Password | SHA-256 only |

Required request headers:

```text
X-Yuanli-Client: ray-primary
Authorization: Bearer <secret from 1Password>
```

Admission behavior:

- unknown client → 403
- missing bearer → 401 + WWW-Authenticate
- invalid bearer → 401
- valid client + bearer → MCP protocol admitted

## Non-authorities

Client admission does **not** grant:

- Canon write
- Knowledge promotion
- Decision authority
- Action execution
- Secret read-through
- Production promotion

## Audit

The runtime emits structured events with schema `yos.net1.auth.audit.v1`:

- `AUTH_DENY`
- `AUTH_ADMIT`

No bearer token is logged.

## Rotation

Rotate by:
1. create/replace the 1Password client credential;
2. compute the new SHA-256 verifier locally without revealing the secret;
3. update the verifier in the governed branch;
4. deploy;
5. run negative + positive admission tests;
6. revoke the old credential.
