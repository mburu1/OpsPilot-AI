# Schema Design and Data Dictionary

**Status:** conceptual proposal. Reconcile this document with actual Django models and migrations when implementation is available. See [erd.md](erd.md).

## Modeling conventions
- Prefer UUID primary keys for externally referenced domain records unless implementation constraints justify another key.
- Use timezone-aware timestamps and store instants in UTC.
- Add created/updated timestamps to mutable domain records where useful.
- Make tenant ownership explicit or unambiguously derivable through a constrained parent relationship.
- Use JSONB for variable metadata, not as a substitute for well-defined relational fields.
- Define finite status values and validate state transitions in the application layer.
- Keep secrets and large raw payloads out of routine API responses.

## Proposed logical entities

| Entity | Purpose | Key fields and constraints |
|---|---|---|
| Organization | Tenant boundary | ID, name, normalized unique slug |
| Account | User identity | ID, normalized unique email; model organization membership explicitly if users can join multiple organizations |
| Service | Monitored application/component | ID, organization ID, name, stable key unique within organization |
| Event | Ingested operational signal | ID, organization ID, service ID, occurrence time, level, source ID, deduplication fingerprint, sanitized attributes |
| Incident | Correlated operational problem | ID, organization ID, status, priority, title, opened/closed timestamps, optional assignee |
| IncidentEvent | Incident-to-event association | Incident ID, event ID, unique pair |
| Investigation | Versioned investigation run | ID, organization ID, incident ID, status, model/provider metadata, summary, confidence, start/completion times |
| EvidenceReference | Provenance for a finding | Investigation ID, source type/ID, excerpt or hash, retrieval metadata, relevance score |
| KnowledgeArticle | Curated operational knowledge | ID, optional organization ID, title, body, source, version, publication state |
| AuditEvent | Security-sensitive action record | Actor, organization, action, resource, timestamp, correlation ID, minimal non-secret metadata |

These are logical design entities, not a claim that corresponding tables exist. The current ERD is simplified and should evolve with the domain model.

## Relationships and integrity
- An organization owns its services and tenant-specific operational data.
- Ensure a referenced service and its event/incident belong to the same organization.
- Incidents may correlate to many events; use an explicit join entity if an event can be linked to multiple incidents.
- An incident may have multiple investigation runs. Preserve historical runs rather than overwriting them.
- Evidence references should identify source material and retrieval time.
- Define whether knowledge articles are global or tenant-specific and prevent cross-tenant retrieval.
- Choose deletion behavior explicitly; protect audit/evidence records where appropriate.

## Indexing guidance
Validate indexes against real query patterns. Candidate indexes include organization plus creation time for tenant lists; organization/status/priority for incident queues; service plus occurrence time for timelines; and a unique organization/source/fingerprint constraint when it matches deduplication semantics. Index high-use foreign keys as needed.

Use EXPLAIN (ANALYZE, BUFFERS) in a representative environment. Consider time-based partitioning only when measured event volume and retention needs justify its operational cost.

## PostgreSQL and pgvector
Treat PostgreSQL as the source of truth for domain state. Each embedding should retain a durable link to its source document/chunk, embedding model/version, and tenant scope. Version re-embedding work so vectors from different models are not silently mixed. Select vector indexes and distance metrics only after workload testing.
