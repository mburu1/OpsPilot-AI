# ADR-001: Modular monolith with independently scalable workers

- **Status:** Proposed by project specification; implementation unverified
- **Date:** 2026-10-19

## Context

OpsPilot AI combines incident lifecycle workflows, event processing, knowledge retrieval, AI investigations, audit history, and reporting. The specification calls for clear domain boundaries without beginning with a large collection of microservices.

## Decision

Use Django as a modular monolith for domain rules and transactional workflows. Use Celery workers as separately scalable processes for long-running or retryable tasks such as event correlation, document indexing, embedding generation, AI investigations, and report generation.

## Consequences

- Domain rules remain in one application boundary and can share transactional persistence.
- Worker concurrency can scale independently from web requests.
- Modules should have explicit responsibilities and avoid unnecessary cross-module coupling.
- Task delivery, retries, idempotency, and database-to-queue consistency require deliberate design.
- Splitting into services should require evidence that a boundary or scaling requirement justifies the operational cost.

## Verification required

Inspect the Django project structure, Celery app and task registrations, and deployment configuration. Update this record if the implementation uses a different execution or service topology.
