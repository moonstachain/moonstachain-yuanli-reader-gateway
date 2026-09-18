# YOS-NET-R2｜Preview × Human Gate × Promotion Contract

Date: 2026-09-18  
Task: `YOS-NET-R2-T1`

## Frozen production baseline

Production deploy before R2:

`6aacc13a48646f1e45068933`

State at freeze:

- context: `production`
- state: `ready`
- site SSO: enabled
- routes: `/mcp`, `/yuanli-context`

R2 MUST NOT mutate this production deploy before the Promotion Human Gate.

## Preview candidate delta

The candidate intentionally changes only governance-visible behavior:

1. keep governed `/mcp`;
2. remove legacy `/yuanli-context` bypass;
3. add the static marker `R2_PREVIEW_CANDIDATE`;
4. do not weaken MCP auth, rate limit, or site access controls.

## Preview acceptance gates

All must pass before Promotion can even be proposed:

- deploy context is non-production;
- unique preview/draft URL exists;
- deploy state is ready;
- static marker is visible in Preview;
- `/mcp` exists;
- `/yuanli-context` is absent;
- Production deploy ID is still `6aacc13a48646f1e45068933`;
- Production URL behavior is unchanged;
- Preview evidence is written back before promotion.

## Promotion Human Gate

Promotion is forbidden until RAY sees:

- Preview URL;
- exact candidate diff;
- acceptance results;
- remaining risks;
- rollback target.

Allowed decisions:

- `PROMOTE`
- `REVISE`
- `REJECT`
- `DEFER`

No prior broad authorization substitutes for this gate.

## Rollback target

If a later production promotion fails, rollback target is the frozen production deploy:

`6aacc13a48646f1e45068933`

## R1 learning reuse test

This R2 task loaded `NET-R1-LRN-001` before work began.

R2 may only claim **reuse** after:
1. Preview actually runs;
2. the loaded learning is shown to have affected execution;
3. comparable evidence is recorded;
4. non-comparable factors are recorded;
5. Human adjudication occurs.

Until then, status remains:

`LOADED_NOT_YET_REUSED`
