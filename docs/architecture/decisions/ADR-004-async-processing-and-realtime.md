# ADR-004: Asynchronous processing and authorized real-time updates

- **Status:** Specified by README; implementation unverified
- **Date:** 2026-10-19

## Context

Event correlation, document indexing, embedding generation, AI investigation, and postmortem generation may be slow or retryable. Engineers also need live incident updates in the React console.

## Decision

Use Celery for background work, Redis for task coordination and the Django Channels channel layer, and Django Channels over ASGI for WebSocket notifications. Use REST to fetch authoritative resource representations after a minimal notification.

## Consequences

- Long-running AI/provider work does not need to block an HTTP request.
- Tasks need bounded retries, idempotent behavior, observable failure states, and queue monitoring.
- WebSocket authentication and tenant-scoped subscriptions must be enforced.
- Notifications should avoid broadcasting sensitive incident payloads globally.
- The implementation must define reliable dispatch between database commits and task queues; the specification recommends considering a transactional outbox.

## Verification required

Inspect Celery configuration, broker settings, Channels routing and middleware, Redis configuration, task retry policies, and Docker Compose services. Do not assume the outbox pattern is implemented until source code proves it.
