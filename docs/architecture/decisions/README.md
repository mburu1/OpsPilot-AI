# Architecture Decision Records

These ADRs capture decisions explicitly stated or recommended in the attached OpsPilot AI specification. They are design baselines, not evidence that the implementation already exists.

## Index

- [ADR template](adr-template.md) — use this structure for future decisions.

- [ADR-001: Modular monolith with independently scalable workers](ADR-001-modular-monolith.md)
- [ADR-002: PostgreSQL with pgvector as the authoritative data and retrieval store](ADR-002-postgresql-pgvector.md)
- [ADR-003: Evidence-grounded, provider-neutral AI](ADR-003-evidence-grounded-ai.md)
- [ADR-004: Asynchronous processing and authorized real-time updates](ADR-004-async-processing-and-realtime.md)

When implementation code is available, review each ADR against actual dependencies, Django settings, models, task configuration, Channels routing, and deployment files. Update status and consequences where the code differs.
