# Scalability and Performance Strategy

> **Status:** Proposed architecture guidance. The repository README identifies the intended stack, but application source and deployment configuration must be inspected before treating any component or capacity as implemented. Do not interpret examples in this document as measured performance guarantees.

## 1. Goals and design principles

OpsPilot AI must support incident ingestion, event correlation, knowledge indexing, evidence retrieval, AI investigations, and post-incident reporting without allowing expensive workloads to degrade interactive incident-response workflows.

Design for:

- **Independent workload scaling:** scale web requests, background workers, and scheduled work according to their own bottlenecks.
- **Tenant isolation:** tenant filters and authorization must remain enforced at every scale, including workers, caches, vector retrieval, and real-time channels.
- **Backpressure:** bound queues, concurrency, request sizes, and provider calls rather than accepting unlimited work.
- **Measured optimization:** establish workload-specific baselines and service-level objectives before selecting instance sizes or capacity targets.
- **Graceful degradation:** core incident records and investigation history should remain accessible when external AI providers or optional integrations are unavailable.
- **Operational simplicity:** start with a modular Django application and separate worker processes; introduce distributed services only when evidence justifies them.

## 2. Workload profiles

| Workload | Primary bottleneck | Scaling approach |
|---|---|---|
| React application and static assets | Browser/network latency and asset delivery | Production static hosting/CDN; optimize bundles and caching |
| Django REST API | CPU, database connections, query latency, request concurrency | Add stateless web replicas behind a reverse proxy/load balancer; tune workers and connection pools |
| Event ingestion and correlation | Input bursts, parsing CPU, duplicate events, database writes | Validate and batch safely; enqueue expensive processing; scale consumers based on queue age and throughput |
| Celery background tasks | Task duration, concurrency, retries, memory | Separate queues by workload; scale worker pools independently |
| Document parsing and embedding | CPU/memory, file size, provider throughput | Use bounded task concurrency and batch embedding requests where supported |
| AI investigations and report generation | Provider latency, token limits, rate limits, cost | Apply provider-specific concurrency limits, timeouts, budgets, retries, and circuit breaking |
| PostgreSQL and pgvector | Query plans, I/O, locks, index size, connection saturation | Optimize queries/indexes first; tune resources and connection management; consider replicas or partitioning only with evidence |
| Redis | Queue depth, memory, command latency, availability | Set memory/eviction policy appropriate to each use, monitor broker health, and size or isolate workloads as needed |
| WebSocket notifications | Connection count, fan-out, channel-layer capacity | Run multiple ASGI instances with a shared supported channel layer; authorize subscriptions and bound message size |

## 3. Application and worker scaling

### Django web tier

- Keep request handlers bounded. Offload indexing, embedding, long-running investigations, and report generation to asynchronous jobs.
- Avoid process-local authoritative state; use PostgreSQL for durable state and shared infrastructure for coordination.
- Paginate list endpoints, validate query parameters, and avoid unbounded nested serialization.
- Use database transactions for domain invariants and avoid holding transactions open while waiting for network or model-provider calls.
- Tune ASGI/WSGI process configuration, worker counts, and database connection limits using load tests. Do not multiply workers without accounting for the total PostgreSQL connection budget.
- Cache only data with a clear invalidation and authorization model. Never use a cache key that can return one tenant's data to another tenant.

### Celery workers

Use separate queues or worker pools for materially different profiles, for example:

- `events`: event normalization, deduplication, and correlation.
- `indexing`: document parsing, chunking, and embedding.
- `investigations`: LLM-backed analysis and evidence synthesis.
- `reports`: post-incident report generation.

These are proposed logical queues, not claims that they already exist. Introduce them only with explicit routing and deployment configuration.

For every task class:

1. Define a timeout and maximum retry policy.
2. Make retries safe through idempotency keys or durable task state.
3. Record task status, attempt count, timestamps, and a sanitized failure reason.
4. Apply per-provider concurrency and rate limits.
5. Route exhausted failures to a monitored recovery path supported by the chosen broker and Celery configuration.
6. Avoid logging credentials, full sensitive payloads, or unnecessary incident data.

### Queue-based backpressure

Monitor queue depth **and oldest-message age**. Depth alone can be misleading when task duration varies. When demand exceeds capacity, apply bounded admission, rate limiting, prioritization, and clear client-visible status rather than allowing unbounded resource consumption.

## 4. PostgreSQL and pgvector

PostgreSQL is the proposed authoritative store for transactional domain records and vector retrieval.

- Add indexes based on real query predicates, joins, ordering, and tenant-scoped access patterns.
- Use `EXPLAIN (ANALYZE, BUFFERS)` against representative safe datasets to investigate expensive queries.
- Track connection saturation, lock waits, transaction duration, deadlocks, slow queries, disk utilization, vacuum health, and replication lag if replicas are introduced.
- Evaluate vector index type and parameters against a representative retrieval benchmark, balancing recall, latency, memory, and update cost.
- Apply tenant and document-access filters as authorization requirements. A high similarity score must never override access control.
- Keep migrations for extensions, vector columns, and indexes explicit and repeatable.
- Consider table partitioning, read replicas, or a dedicated retrieval service only after profiling shows the simpler design is insufficient. Account for consistency, migration, and operational costs.

Do not add indexes indiscriminately: each index increases storage and write/maintenance overhead.

## 5. Caching

Potential cache candidates include short-lived reference data, stable configuration, and expensive non-sensitive derived results. For each cache, document:

- Key structure, including tenant and authorization scope where applicable.
- TTL and invalidation behavior.
- Maximum memory and eviction policy.
- Whether stale data is acceptable.
- Behavior when Redis or the cache is unavailable.

Do not cache authorization decisions or incident data across users or tenants without a deliberate security and invalidation design. Cache misses must remain correct, even if slower.

## 6. External AI provider controls

AI workloads have variable latency and external quotas. Provider adapters should support:

- Connection and overall request timeouts.
- Bounded concurrency and provider-specific rate limits.
- Retries only for transient failures, with exponential backoff and jitter.
- Circuit breaking or equivalent protection during sustained provider failure.
- Token/context limits, maximum output sizes, and configurable per-investigation budgets.
- Cancellation and durable status transitions for work that cannot complete.
- Versioned prompts/models and a repeatable quality benchmark.

Do not retry validation failures or permanent authorization errors as if they were transient. Keep AI-generated hypotheses separate from verified incident facts, and require human authorization for production remediation.

## 7. Real-time delivery

Use WebSockets for small, authorized notifications rather than treating them as the canonical source of incident state.

- Authenticate connections and authorize each tenant/resource subscription.
- Send minimal event identifiers and versions; clients fetch authoritative state through authorized REST endpoints.
- Handle reconnects, missed notifications, duplicate messages, and stale versions.
- Bound connection counts and message sizes; avoid global broadcasts containing sensitive incident details.
- Monitor active connections, disconnects, send failures, channel-layer latency, and fan-out volume.

## 8. Capacity planning and load testing

Do not publish capacity figures until the application has been measured. Define a representative workload with realistic tenant distribution, event bursts, incident sizes, documents, concurrent users, vector queries, and AI-provider latency.

Measure at minimum:

- API throughput and p50/p95/p99 latency by endpoint class.
- Error and timeout rates.
- Event ingestion rate and end-to-end processing delay.
- Queue depth, oldest task age, task duration, retries, and failure rate.
- PostgreSQL query latency, connection utilization, lock waits, and resource usage.
- Vector retrieval latency and benchmark quality (for example, recall at a selected (k)).
- AI-provider latency, throttling, token usage, and cost per completed investigation.
- WebSocket connection stability and notification delay.
- Recovery behavior during Redis, database, worker, and provider outages.

Test normal load, expected peaks, sudden bursts, sustained overload, and recovery after an outage. Use production-like but non-sensitive data and avoid load tests against real production dependencies without authorization.

### Scaling decision sequence

1. Establish a baseline and service-level objectives.
2. Identify the measured bottleneck.
3. Optimize queries, algorithms, payloads, and task behavior.
4. Add capacity to the constrained tier and repeat the same test.
5. Introduce caching, partitioning, replicas, or additional service boundaries only when measurements justify the complexity.
6. Record material architecture changes in an ADR and document rollback criteria.

## 9. Reliability and recovery

- Define recovery point and recovery time objectives for durable incident and audit records.
- Back up PostgreSQL and test restoration, including relevant extension and migration requirements.
- Define Redis persistence and recovery expectations separately for broker, cache, and channel-layer usage; do not assume transient notifications are durable business records.
- Ensure queued or retried tasks cannot create duplicate investigations, duplicate audit entries, or inconsistent status transitions.
- Use bounded retries, timeouts, health checks, graceful shutdown, and a documented deployment rollback process.
- Preserve a useful non-AI workflow during provider outages.

## 10. Observability

Use structured, sanitized logs and correlate HTTP requests, incidents, and background tasks with trace/correlation identifiers. Exclude secrets and avoid unnecessary personally identifiable or sensitive operational payloads.

Create dashboards and alerts for:

- API latency/error rate and saturation.
- Database health, query latency, connections, and storage.
- Queue age/depth, task failures, retries, and worker utilization.
- AI provider latency, throttling, availability, and spend.
- Indexing throughput and vector-search quality.
- WebSocket health and notification delay.

Alerts should identify actionable symptoms and include a runbook or recovery action.

## 11. Implementation checklist

- [ ] Define workload classes, expected peaks, and service-level objectives.
- [ ] Establish load-test fixtures and a reproducible baseline.
- [ ] Verify task queues, routing, retry policies, and idempotency in source.
- [ ] Verify tenant isolation across API, workers, caches, vectors, and WebSockets.
- [ ] Add database and queue metrics before scaling decisions.
- [ ] Test provider timeout, rate-limit, and outage behavior.
- [ ] Test backup restoration and task recovery.
- [ ] Record measured results and revisit this strategy as the system evolves.

## Related documentation

- [System architecture](system-architecture.md)
- [Deployment topology](deployment.md)
- [Architecture Decision Records](decisions/README.md)
- [Database indexing strategy](../database/indexing-strategy.md)
- [Database ERD](../database/erd.md)

All components and controls described here remain proposed until verified against implementation, configuration, and test evidence.
