# AI Safety and Limitations

> Status: Proposed safety baseline. Controls described here must be verified in implementation before being represented as active protections.

OpsPilot AI is intended to assist incident investigation. AI output is decision support, not authoritative telemetry, proof of root cause, or permission to make production changes.

## Core safety rules

1. Evidence must take precedence over fluent narrative.
2. Label inferred causes as hypotheses; do not present them as confirmed facts.
3. Treat incomplete, contradictory, and stale evidence as uncertainty.
4. Model output cannot grant permissions or authorize actions.
5. Validate output locally, even when structured generation is requested.
6. Preserve tenant isolation across requests, retrieval, jobs, caches, reports, and real-time channels.
7. Require authorized human approval for high-impact remediation.

## Threat model

| Threat | Required mitigation |
|---|---|
| Prompt injection in logs, tickets, runbooks, or retrieved documents | Treat source content as data; isolate instructions; enforce tool allowlists and output validation |
| Fabricated diagnosis | Evidence citations, deterministic checks, uncertainty labels, human review |
| Cross-tenant retrieval/cache leakage | Tenant-scoped authorization at every boundary and adversarial isolation tests |
| Secret or personal-data exposure | Data minimization, redaction, provider policy, log controls |
| Malicious remediation | No automatic execution by default; least privilege, approval, isolation, rollback |
| Provider outage or malformed output | Timeouts, bounded retries, schema validation, explicit degraded state |
| Stale telemetry or knowledge | Source timestamps, freshness indicators, conflict handling |
| Denial of service or cost abuse | Rate limits, context limits, concurrency controls, quotas, monitoring |

## Evidence integrity

Preserve source IDs, timestamps, origins, and retrieval metadata. Distinguish observed facts, inferred hypotheses, confirmed causes supported by a defined validation process, and inconclusive results. Never invent logs, metrics, links, incident IDs, timestamps, or runbook steps. Surface conflicting evidence and missing information rather than silently choosing a narrative.

## Prompt injection and untrusted content

Logs, issue descriptions, code comments, runbooks, retrieved documents, and provider responses are untrusted data. Keep trusted instructions separate from retrieved content and do not rely on prompt wording as the sole defense. Enforce tool permissions in application code. Validate generated queries, commands, URLs, and structured fields. Never pass model-generated content directly to a shell, SQL execution path, deployment system, or privileged API without an independently authorized and constrained workflow.

## Actions and human approval

The default design should be read-only investigation and recommendations. If remediation is introduced, require explicit user intent, action-specific permission checks, an allowlisted action catalog, parameter validation, dry-run where practical, risk classification, human approval for material changes, idempotency, timeouts, audit records, cancellation, least-privilege credentials, isolation, and recovery guidance. A model recommendation is never user approval, and an AI workflow must not approve its own high-impact action.

## Privacy and tenant isolation

Before sending data to a model, determine whether it is permitted to leave the deployment boundary. Minimize payloads and redact secrets, credentials, and unnecessary personal data. Review provider retention, training, region, and data-processing terms. Restrict access to prompts, outputs, incident records, evaluation traces, and debugging artifacts; define retention explicitly.

Derive tenant scope from an authenticated identity and verified membership, not an unchecked client-supplied tenant ID. Enforce scope in API querysets, services, PostgreSQL/vector retrieval, Celery jobs, caches, report downloads, exports, and Channels subscriptions. Workers must carry verifiable context and re-check access where permissions may have changed. Test cross-tenant access using deliberately similar identifiers and content.

## Output validation

Parse model output as data, validate against a versioned schema, enforce size and field constraints, validate evidence references against retrieved records, and reject or safely repair invalid output within a bounded policy. Schema validity does not prove factual correctness. Escape or allowlist HTML, Markdown, URLs, SQL fragments, shell commands, and code according to their use.

## Known limitations

AI may misread incomplete telemetry, overfit to familiar patterns, miss rare causes, vary between runs, and be sensitive to prompt/model changes. Retrieval may omit relevant or return stale documents. Benchmarks cannot cover every production scenario; provider latency, availability, and cost vary. Confidence language is not a calibrated probability unless measured and validated.

Do not claim guaranteed root-cause accuracy, causal proof from correlation, replacement of incident commanders, or safe autonomous execution of arbitrary remediation.

## Monitoring and incident response

Monitor unsupported-claim findings, invalid citations, schema failures, provider errors, latency, cost, and user-reported issues with appropriate redaction. Provide rollback or disablement for model, prompt, and retrieval changes. Treat suspected data leakage, cross-tenant exposure, unsafe execution, or secret disclosure as security incidents: disable the affected path, preserve restricted evidence, notify owners, investigate scope, remediate, and add regression tests before re-enabling it.

## Release checklist

- [ ] Threat model reviewed.
- [ ] Evidence provenance and uncertainty behavior tested.
- [ ] Prompt-injection and output-validation tests pass.
- [ ] Tenant isolation covered across API, retrieval, jobs, caches, channels, and reports.
- [ ] Provider data handling and retention reviewed.
- [ ] Sensitive values excluded from normal logs.
- [ ] High-impact actions require independent authorization and approval.
- [ ] Evaluation results, limitations, and rollback are documented.
