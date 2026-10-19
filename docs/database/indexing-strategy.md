# PostgreSQL Indexing Strategy

**Status:** proposed database design guidance. Validate all indexes against implemented Django models, representative data volumes, and measured query plans before production rollout.

## Objectives

Indexes should improve common read paths without imposing excessive write amplification, storage consumption, vacuum overhead, or migration locks. PostgreSQL automatically creates indexes for primary-key and unique constraints, but does not automatically index every foreign-key column on the referencing table.

Treat this as a workload-driven strategy, not a requirement to create every candidate index listed below.

## Query patterns to support

Prioritize and measure these likely OpsPilot AI access patterns:

1. List incidents within one organization, filtered by status and/or priority, ordered by most recently updated.
2. Load one incident and its investigation history.
3. Retrieve an event timeline for a service or incident over a time interval.
4. Deduplicate repeated incoming events by source and fingerprint.
5. Find evidence and knowledge chunks for a tenant-scoped investigation.
6. Load audit events for an organization, actor, resource, or time interval.
7. Process queued records without repeatedly scanning large tables.

Record expected query frequency, result cardinality, latency target, and write rate for each critical pattern. Validate using production-like data distributions, not just a tiny development database.

## Candidate B-tree indexes

The names below are logical examples. Translate them into Django Meta.indexes, UniqueConstraint, or reviewed migrations using actual model and field names.

| Table / logical entity | Candidate index | Intended workload | Notes |
|---|---|---|---|
| Incident | (organization_id, status, updated_at DESC) | Organization-scoped status queues | Check whether priority needs a separate index |
| Incident | (organization_id, priority, updated_at DESC) | Priority-based incident queues | Add only if filtering is frequent and selective |
| Event | (service_id, occurred_at DESC) | Service event timeline | Match the actual query predicates |
| Event | (organization_id, occurred_at DESC) | Tenant-wide event searches | Consider partitioning separately if volume warrants it |
| IncidentEvent | Unique (incident_id, event_id) | Prevent duplicate associations | Unique constraint creates its supporting index |
| IncidentEvent | (event_id, incident_id) | Reverse lookup from event to incidents | Add if reverse traversal is frequent |
| Investigation | (incident_id, created_at DESC) | Investigation history | Consider organization scope when used in queries |
| EvidenceReference | (investigation_id, created_at) | Evidence for an investigation | Match actual sort/filter behavior |
| KnowledgeArticle | (organization_id, publication_state, updated_at DESC) | Tenant-scoped knowledge listings | Define global versus tenant-owned articles |
| AuditEvent | (organization_id, occurred_at DESC) | Tenant audit history | Keep audit records append-oriented where practical |
| AuditEvent | (actor_id, occurred_at DESC) | Actor investigation | Add only if required and frequent |

Use real timestamp and field names from implemented models. Avoid overlapping indexes automatically: a composite index may already cover a left-prefix query, depending on predicates, ordering, and PostgreSQL's chosen plan.

### Composite index column order

For a B-tree index, order columns according to equality filters, range predicates, and requested ordering. A common starting point is equality-constrained columns first, followed by range/order columns, but verify the actual query plan. The most selective column is not automatically the correct first column in every composite index.

For example, an index on (organization_id, status, updated_at DESC) can support queries that constrain organization_id and status and order by updated_at. It is not equivalent to an index led by status for every workload.

## Uniqueness and idempotency

Use database-enforced uniqueness where it reflects a true domain invariant. A possible event deduplication constraint is (organization_id, source, fingerprint).

Apply it only if fingerprint definition and source identity are stable, and define behavior for null values and legitimate repeated events. PostgreSQL unique constraints treat nulls as distinct by default unless configured otherwise. Application-level check-then-insert logic alone does not prevent concurrent duplicates.

Use unique constraints for normalized account email or service keys only after deciding whether uniqueness is global or organization-scoped and how normalization is enforced.

## Partial and covering indexes

### Partial indexes

Partial indexes can reduce index size when a query repeatedly targets a stable subset, such as unresolved incidents. An example predicate is WHERE status IN ('open', 'investigating').

Create a partial index only when the query predicate implies the index predicate and the targeted subset is materially smaller. Frequently changing predicates can increase maintenance and complicate planning.

### Covering indexes

INCLUDE columns can support index-only scans when PostgreSQL visibility-map conditions permit them. They increase index size and write cost. Use them only after plans demonstrate that heap reads are a meaningful bottleneck. Do not include large text, JSONB payloads, or sensitive content merely to make an index covering.

## JSONB and full-text search

- Add a GIN index for JSONB only when actual queries use operators supported by the selected operator class and the workload justifies its cost.
- Choose jsonb_ops versus jsonb_path_ops based on required operators; they do not support identical query capabilities.
- For textual search across incident summaries or knowledge articles, evaluate PostgreSQL full-text search with a suitable text-search configuration and search vector.
- Do not assume a normal B-tree index accelerates arbitrary substring matching.
- Avoid indexing every dynamic metadata key. Promote frequently filtered, stable attributes to typed columns when justified.

## pgvector indexes

Vector indexing depends on embedding dimensions, distance metric, pgvector version, data volume, tenant distribution, and recall/latency targets.

1. Persist embedding model/version and the source document or chunk identifier.
2. Apply tenant and authorization filters as part of retrieval, not after returning unrestricted candidates.
3. Benchmark exact nearest-neighbor search first as a baseline.
4. Compare supported approximate indexes, such as HNSW or IVFFlat, using representative data and the configured metric.
5. Measure recall, latency, index build time, memory, disk use, and insert/update cost.
6. Re-test filtered retrieval at realistic tenant sizes.
7. Plan index rebuilding when embedding dimensions, models, or distance semantics change.

Verify the installed PostgreSQL and pgvector versions and supported syntax before selecting an index or operator class.

## High-volume event tables and partitioning

Consider time-based partitioning only after event volume, retention, vacuum behavior, or maintenance windows demonstrate a need. Partitioning adds constraints around unique keys, foreign keys, migrations, and query planning.

Before adopting it, decide the partition key and interval, cross-partition uniqueness strategy, late-arriving event handling, retention/archive process, partition pruning requirements, and how migrations, backups, restores, and tests handle partitions.

Partitioning is not a substitute for suitable indexes or a clear retention policy.

## Validation workflow

### 1. Inspect actual query plans

Use representative staging data and parameter values. This read-only diagnostic query is an example; replace names and the test organization identifier with the actual schema.

    EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
    SELECT id, status, priority, updated_at
    FROM incident
    WHERE organization_id = 'replace-with-test-organization-id'
      AND status = 'open'
    ORDER BY updated_at DESC
    LIMIT 50;

EXPLAIN ANALYZE executes the statement; use extra caution with mutating statements. Examine estimated versus actual row counts, scan type, sort cost, shared buffer hits/reads, and loops.

### 2. Inspect index usage and size

Example read-only diagnostics:

    SELECT
        schemaname,
        relname AS table_name,
        indexrelname AS index_name,
        idx_scan,
        pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
    FROM pg_stat_user_indexes
    ORDER BY pg_relation_size(indexrelid) DESC;

    SELECT
        schemaname,
        relname AS table_name,
        seq_scan,
        idx_scan,
        n_live_tup
    FROM pg_stat_user_tables
    ORDER BY seq_scan DESC;

Statistics are cumulative and can reset; interpret them over a known observation window. A high sequential-scan count is not automatically bad: sequential scans can be optimal for small tables or queries returning a large fraction of rows. Confirm permissions and monitoring configuration before relying on additional statistics.

### 3. Measure before and after

- Capture baseline p50/p95/p99 latency and representative query plans.
- Compare realistic data volume and concurrent write traffic.
- Include insert/update throughput, index size, lock duration, and vacuum impact.
- Confirm results after statistics are current; run ANALYZE in a suitable non-production or controlled environment.
- Retain an index only when its measured benefit justifies its ongoing cost.

## Django implementation guidance

Use explicit, named indexes and constraints in model Meta definitions where possible. Generate and review migrations, inspect SQL with sqlmigrate, and test against the supported PostgreSQL version.

For large production tables, evaluate PostgreSQL concurrent index-build options and Django migration support. Concurrent builds have operational caveats and cannot be treated like an ordinary transactional index operation; review the generated migration and deployment procedure before use.

Do not drop an index solely because its usage counter is low over a short window. Check critical business queries, constraints, maintenance windows, and longer observation periods first.

## Operational checklist

- [ ] Critical query patterns and latency targets are documented.
- [ ] Indexes are justified by measured plans or a clear integrity requirement.
- [ ] Foreign-key traversal paths have been reviewed.
- [ ] Unique constraints protect idempotency and domain invariants.
- [ ] Tenant filters are included in queries and retrieval paths.
- [ ] JSONB, full-text, and vector indexes are workload-specific.
- [ ] Index size and usage are monitored over a meaningful period.
- [ ] Migration lock and rollback/forward-fix procedures are reviewed.
- [ ] Retention and partitioning decisions align with recovery and lifecycle policies.
- [ ] Changes are benchmarked under representative read/write load.

## Related documents

- [Database documentation index](README.md)
- [Entity relationship diagram](erd.md)
- [Schema design and data dictionary](schema-design.md)
- [Migrations and seed data](migrations.md)
- [Security, tenancy, and retention](security-tenancy-retention.md)
