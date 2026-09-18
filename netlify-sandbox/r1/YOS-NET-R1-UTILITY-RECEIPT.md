# YOS-NET-R1｜Reality & Utility Receipt

Date: 2026-09-18  
Status: **PASS_BOUNDED_CURRENT_TASK_UTILITY**

## 1. One Real Brain Read

**PASS.**

The read used the existing pinned GBrain runtime rather than a file grep presented as Brain recall.

Observed:
- GBrain: `0.42.57.0`
- engine: `PGLite`
- source: `soul`
- indexed pages: `1001`
- source last sync: `2026-09-16T10:11:52.013Z`

Two controlled maintenance reads were executed against the real PGLite brain. After each, the launchd-managed GBrain service was restored. Final local checks:

```text
127.0.0.1:3131 /health → status=ok
127.0.0.1:3132 /health → status=ok
```

The existing GBrainHub gateway is already a governed read surface with a read-tool allowlist. Its tailnet URL was also probed in this run, but the TLS probe failed from the current machine; therefore **external tailnet reachability is not claimed by R1**.

## 2. Recall behavior observed

### Broad / composite batch

```text
queries   = 4
non-empty = 1
empty     = 3
observed hit rate = 25%
```

### Bounded / atomic batch

```text
queries   = 4
non-empty = 4
empty     = 0
observed hit rate = 100%
```

This is a task-local observation, **not** a universal GBrain recall benchmark.

### Retrieval learning candidate

> For this class of strategic recall, decompose broad mixed questions into bounded atomic queries before retrieval. A composite-query miss is not evidence that the Brain lacks the knowledge.

## 3. Context that materially changed the task

The Brain recovered existing governance that was absent from the pre-read plan:

- no second real task preload → no Reuse / Compounding claim;
- a later independent Task2 is required;
- approved learning must be fixed before Task2;
- Task2LoadReceipt is required;
- comparable metrics and non-comparable factors must both be recorded;
- authorized human adjudication remains required;
- system-learning result and business outcome remain separate.

## 4. One Real Outcome

A live project decision changed **before additional NET build-out**.

### BEFORE Brain Read

```text
Build a NET-specific A/B around:
Recall Utility
Context Quality
Outcome Lift
```

### AFTER Brain Read

```text
Do not invent a new NET compounding rubric.

Reuse the existing Yuanli Task2 / Reuse governance.

R1 proves only bounded current-task Utility:
Real Brain Context changed a current implementation decision.

Reuse / Compounding remain reserved for:
later independent Task2
+ preload before task
+ Task2LoadReceipt
+ comparable evidence
+ Human adjudication
```

### Concrete value created

This read prevented:
1. duplicate evaluation architecture;
2. a false-green claim that same-task before/after comparison proves compounding;
3. premature business-outcome attribution.

## 5. Existing evaluator was reused

The existing deterministic `scripts/task2_uplift_evaluator.py` was run against the current R1 task.

It returned:

```json
{
  "state": "BLOCKED",
  "reason_code": "LATER_TASK_REQUIRED"
}
```

That is the correct verdict and is itself evidence that the Brain-recalled governance changed the project in the right direction.

## 6. Utility verdict

### Proven in R1

- real GBrain read occurred;
- previously existing relevant Context was recalled;
- recalled Context changed a live project decision before further action;
- the read prevented reinvention and false-green promotion;
- a bounded learning candidate has been produced for a later task.

### Explicitly not proven

- live Netlify → GBrain connectivity;
- generic external-client interoperability;
- business outcome uplift;
- Reuse;
- Compounding;
- general OS self-improvement.

## 7. Strategic meaning

R1 upgrades the NET project from:

```text
Governed Capability Plane
```

to the first evidence of:

```text
Used Capability Plane
```

but **not yet** to Compounding Capability Plane.

The next valid proof must load the candidate learning into a later independent task before execution.
