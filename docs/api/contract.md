# OpsPilot AI API Contract (Proposed)

> **Status:** derived from the attached specification; not generated from implemented DRF routes. These endpoints are a proposed contract and must be reconciled with serializers, permissions, URL routing, and the generated OpenAPI schema.

## REST endpoints

Base path: `/api/v1/`

| Method | Path | Purpose | Expected behavior |
|---|---|---|---|
| POST | `/events/ingest` | Ingest operational event(s) | Validate, tenant-authorize, deduplicate, persist, enqueue processing |
| GET | `/incidents` | List incidents | Tenant-scoped filtering and pagination |
| GET | `/incidents/{id}` | Read incident detail and timeline | Return only authorized incident data |
| POST | `/incidents/{id}/acknowledge` | Acknowledge incident | Validate lifecycle transition and record audit event |
| POST | `/incidents/{id}/investigations` | Queue AI investigation | Return accepted job identifier/status |
| GET | `/investigations/{id}` | Read investigation state/result | Tenant-scoped job state and evidence-linked output |
| POST | `/hypotheses/{id}/feedback` | Accept/reject/correct hypothesis | Record human decision and audit history |
| POST | `/knowledge/documents` | Submit knowledge document | Validate size/type and queue indexing |
| GET | `/knowledge/search` | Search authorized knowledge | Apply tenant/source permissions before returning passages |
| POST | `/incidents/{id}/postmortems` | Generate postmortem draft | Queue generation or return existing draft according to implementation |
| GET | `/services` | List monitored services | Tenant-scoped service inventory |
| GET | `/analytics/reliability` | Read reliability metrics | Return documented aggregation window and metric definitions |

## Contract requirements

- Authentication and tenant authorization on every tenant-owned resource.
- Consistent error representation, request/correlation ID, input validation, pagination limits, and payload size limits.
- Idempotency behavior for event ingestion must be explicitly documented.
- Long-running work should return a job identifier and a defined pending/running/succeeded/failed state model.
- Do not expose raw provider secrets, internal prompts, unauthorized source content, or cross-tenant metadata.
- WebSocket notifications should be minimal; clients fetch authoritative data through REST.
- Generate the production OpenAPI document from DRF once routes and serializers exist. Treat that generated schema as the API source of truth.

## Illustrative WebSocket notification

```json
{
  "type": "investigation.completed",
  "incident_id": "incident-123",
  "investigation_id": "investigation-456",
  "occurred_at": "2026-10-19T10:30:00Z"
}
```

The identifiers and timestamp are illustrative. Actual field names, serialization, event types, authentication, and Channels group names remain unverified.

## OpenAPI validation checklist

- [ ] Every route is represented in the generated schema.
- [ ] Request and response serializers match the schema.
- [ ] Authentication and permissions are represented where applicable.
- [ ] Error responses and pagination are consistent.
- [ ] Frontend types are generated or checked against the schema.
- [ ] Contract and tenant-isolation tests cover success and failure paths.
