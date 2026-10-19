# Architecture Decisions — OpsPilot AI

> **Document status:** Proposed architecture baseline  
> **Last reviewed:** 2026-10-19  
> **Scope:** System-wide architectural decisions for the intended OpsPilot AI platform.

This document is the high-level decision register for OpsPilot AI. It summarizes the architectural choices that shape the system and links to the detailed Architecture Decision Records (ADRs).

**Important:** The repository describes a proposed full-stack platform. Architecture documentation is not proof that the corresponding application code, infrastructure, or operational controls have been implemented or tested. Revisit each decision during implementation and record deviations with evidence.

## 1. Decision principles

Architecture decisions should:

1. State the context and problem before selecting a solution.
2. Record the decision, alternatives considered, and material trade-offs.
3. Prefer the simplest design that satisfies security, reliability, and product requirements.
4. Keep evidence, authorization, tenant isolation, and auditability as cross-cutting requirements.
5. Distinguish a design intention from a verified implementation.
6. Be revisited when measured operational evidence or requirements materially change.
7. Preserve history: supersede an ADR rather than silently rewriting a previously accepted decision.

## 2. Decision status

| Status | Meaning |
|---|---|
| Proposed | A recommended direction awaiting review or implementation validation. |
| Accepted | Approved as the current design baseline. |
| Implemented | Verified in source/configuration and covered by appropriate tests. |
| Superseded | Replaced by a later ADR; retain the record and link to its replacement. |
| Rejected | Considered and explicitly not selected; record the rationale. |

The ADRs linked below document the intended architecture. Unless implementation evidence is recorded in the individual ADR, do not infer that a decision is implemented merely because its document exists.

## 3. Decision register

| ID | Decision | Rationale / key consequence | Detailed record |
|---|---|---|---|
| ADR-001 | Use a modular Django monolith with independently scalable background workers. | Keeps domain boundaries explicit without premature microservice overhead; long-running work can scale separately from web requests. | [ADR-001: Modular monolith with independently scalable workers](decisions/ADR-001-modular-monolith.md) |
| ADR-002 | Use PostgreSQL with pgvector as the authoritative relational and vector-retrieval store. | Keeps transactional records and vector retrieval close together while preserving relational constraints and tenant-scoped queries. | [ADR-002: PostgreSQL with pgvector](decisions/ADR-002-postgresql-pgvector.md) |
| ADR-003 | Use evidence-grounded, provider-neutral AI integrations. | Separates provider-specific SDKs from investigation workflows and makes claims traceable to evidence; model output remains a hypothesis until validated. | [ADR-003: Evidence-grounded, provider-neutral AI](decisions/ADR-003-evidence-grounded-ai.md) |
| ADR-004 | Run long-running work asynchronously and authorize real-time updates. | Protects request latency, supports retries and workload isolation, and requires WebSocket/channel authorization to preserve tenant boundaries. | [ADR-004: Asynchronous processing and authorized real-time updates](decisions/ADR-004-async-processing-and-realtime.md) |

### Related architecture guidance

- [System architecture](system-architecture.md) — conceptual components and request/data flow.
- [Dependency rules](dependency-rules.md) — intended dependency direction and module boundaries.
- [Scalability strategy](scalability.md) — workload separation, scaling, backpressure, and performance validation.
- [Deployment topology](deployment.md) — intended runtime and deployment concerns.
- [ADR index and template](decisions/README.md) — detailed decision records and the template for new ADRs.

## 4. Cross-cutting constraints

The following requirements apply to every decision and implementation:

### Evidence integrity

- Preserve source identifiers and provenance for operational evidence.
- Distinguish observed facts, inferred hypotheses, and confirmed root causes.
- Do not let a generated narrative silently replace or mutate original telemetry or source records.
- Record the evidence and validation path used to support material conclusions.

### Security and tenant isolation

- Enforce tenant and user authorization on API requests, background tasks, retrieval queries, caches, exports, and real-time subscriptions.
- Treat event payloads, uploaded documents, logs, and retrieved knowledge as untrusted input.
- Keep secrets in deployment-managed secret configuration; never commit credentials or log them.
- Require explicit authorization and human approval for production-changing actions.
- Minimize sensitive data sent to external AI providers and apply configured redaction policies.

### Reliability and operations

- Make retried background operations idempotent where practical.
- Bound task duration, retries, concurrency, payload sizes, and provider spending.
- Define timeouts and safe failure behavior for external integrations.
- Use structured, sanitized logs and observable task/run states.
- Preserve access to durable incident records when optional AI providers are unavailable.
- Establish performance baselines and service-level objectives before claiming capacity or latency guarantees.

### API and frontend contracts

- Treat API and WebSocket schemas as versioned contracts.
- Generate or validate API documentation against implemented Django REST Framework routes when available.
- Keep frontend code dependent on published contracts rather than backend implementation details.
- Define pagination, validation errors, authentication behavior, and compatibility expectations explicitly.

## 5. How to add or change a decision

1. Confirm the problem and the requirement that makes a decision necessary.
2. Inspect the current source, settings, tests, and deployment configuration before describing existing behavior.
3. Add a new record using [the ADR template](decisions/adr-template.md).
4. Give it the next available sequential identifier: `ADR-NNN-short-title.md`.
5. Include context, decision, alternatives, consequences, security/reliability implications, and validation evidence.
6. Update the decision register and relevant architecture diagrams or implementation documentation.
7. Have the relevant technical owner review the decision.
8. When a decision changes, create a replacement ADR and mark the previous record **Superseded**, with a link to its successor.

Do not mark a decision **Implemented** until the relevant code/configuration and verification evidence have been inspected. Evidence may include tests, migration history, dependency checks, deployment configuration, threat-model review, or measured load-test results, as appropriate to the decision.

## 6. Review triggers

Revisit the register when any of the following occurs:

- A domain boundary or ownership model changes.
- A new persistence engine, queue, AI provider, or external integration is introduced.
- Tenant isolation, authentication, authorization, or data-retention requirements change.
- Load testing reveals a bottleneck that cannot be addressed within the current topology.
- A provider outage, data-integrity issue, security finding, or operational incident invalidates an assumption.
- Implementation diverges materially from the documented design.

## 7. Acceptance checklist

Before treating an ADR as accepted, verify that it:

- [ ] Describes the context and problem clearly.
- [ ] Records the decision and the alternatives considered.
- [ ] Explains positive and negative consequences.
- [ ] Addresses security, privacy, tenant isolation, and failure behavior where relevant.
- [ ] Identifies implementation and verification work.
- [ ] Links to related ADRs and architecture documentation.
- [ ] Uses a status that accurately reflects the available evidence.

---

**Maintenance rule:** Keep this register concise and navigational. Detailed reasoning belongs in the individual ADR files; implementation-specific claims belong in code-derived documentation and must be verified.
