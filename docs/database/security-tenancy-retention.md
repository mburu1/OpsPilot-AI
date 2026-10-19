# Database Security, Tenant Isolation, and Retention

**Status:** proposed controls. Verify them against implemented Django models, API permissions, Celery tasks, and deployment settings before claiming compliance.

## Tenant isolation
1. Derive the active organization from authenticated, authorized membership—not an untrusted request field alone.
2. Scope every tenant-owned queryset before retrieving or mutating data.
3. Apply the same checks to DRF detail views, search, exports, websocket subscriptions, and admin actions.
4. Pass explicit tenant context into Celery tasks and re-check scope when tasks execute. A task ID is not authorization.
5. Scope RAG and vector searches by tenant before returning evidence.
6. Test that users in organization A cannot read, infer, mutate, delete, or retrieve organization B data.
7. Restrict cross-tenant operator access to explicitly authorized and audited workflows.

PostgreSQL row-level security may provide defense in depth. If enabled, define how pooled connections set and clear tenant context to prevent leakage between requests.

## Credentials and database permissions
- Use least-privilege runtime database roles; separate migration privileges where practical.
- Require encrypted database connections in production and restrict network access.
- Keep credentials in a secret manager or deployment environment, never committed settings.
- Rotate and revoke credentials through a documented process.
- Use parameterized ORM/query APIs; never concatenate untrusted input into SQL.
- Restrict access to database consoles, backups, and exports.

## AI evidence and sensitive data
- Minimize event payloads and redact credentials, authorization headers, personal data, and secrets at ingestion.
- Treat logs, tickets, and retrieved documents as untrusted input; they cannot override system policy or authorize actions.
- Store source identifiers and timestamps for traceability without unnecessary duplication of sensitive content.
- Record model/provider and pipeline versions when needed for reproducibility, without logging secrets.
- Label confidence and root-cause status explicitly. AI-generated hypotheses are not verified facts.
- Require explicit authorization and human approval before production changes or high-impact remediation.

## Retention and deletion
Define retention periods per data class before production:

| Data class | Policy to define |
|---|---|
| Raw events and telemetry | Retention window, archive/partition strategy, payload handling |
| Incidents and investigations | Operational/audit retention and preservation of investigation versions |
| Evidence and retrieved chunks | Source deletion propagation, embedding invalidation, re-indexing |
| Audit events | Security, contractual, and legal retention requirements |
| Backups and exports | Expiry, encryption, access controls, deletion schedule |

Deletion must account for embeddings, caches, exports, and queued jobs. Document legal holds and tenant offboarding. Do not promise complete deletion until copies and retention exceptions are addressed.

## Backup and recovery
- Define recovery point objective (RPO) and recovery time objective (RTO).
- Automate encrypted backups and restrict access separately from application access.
- Test restores regularly in an isolated environment.
- Monitor backup freshness and failures.
- Verify PostgreSQL WAL/archive configuration if point-in-time recovery is required.
- Treat successful backup completion as insufficient until restore has been tested.

## Production verification
- [ ] Tenant isolation tests cover HTTP, background jobs, websockets, and vector retrieval.
- [ ] Sensitive payloads and secrets are redacted from logs.
- [ ] Runtime database permissions follow least privilege.
- [ ] Retention covers derived data and backups.
- [ ] Restore procedures are tested and RPO/RTO are approved.
- [ ] Security-sensitive actions are auditable without logging secrets.
