# OpsPilot AI — Conceptual Entity-Relationship Diagram

> **Conceptual proposal, not a schema extraction.** The repository had no application source or migrations when this was authored. Entity and relationship names below are inferred from the attached specification and must be reconciled with actual Django models before being treated as the implemented schema.

## ERD

```mermaid
erDiagram
    ORGANIZATION ||--o{ MEMBERSHIP : has
    USER ||--o{ MEMBERSHIP : joins
    ORGANIZATION ||--o{ SERVICE : owns
    SERVICE ||--o{ SERVICE_DEPENDENCY : source
    SERVICE ||--o{ SERVICE_DEPENDENCY : target
    ORGANIZATION ||--o{ INCIDENT : scopes
    SERVICE ||--o{ INCIDENT : affects
    INCIDENT ||--o{ EVENT : contains
    ORGANIZATION ||--o{ EVENT : scopes
    INCIDENT ||--o{ INVESTIGATION : has
    INVESTIGATION ||--o{ HYPOTHESIS : produces
    HYPOTHESIS ||--o{ HYPOTHESIS_FEEDBACK : receives
    USER ||--o{ HYPOTHESIS_FEEDBACK : submits
    ORGANIZATION ||--o{ KNOWLEDGE_DOCUMENT : owns
    KNOWLEDGE_DOCUMENT ||--o{ DOCUMENT_CHUNK : splits_into
    DOCUMENT_CHUNK ||--o{ EVIDENCE_REFERENCE : cited_by
    INVESTIGATION ||--o{ EVIDENCE_REFERENCE : uses
    INCIDENT ||--o{ POSTMORTEM : documented_by
    INCIDENT ||--o{ AUDIT_EVENT : records
    ORGANIZATION ||--o{ AUDIT_EVENT : scopes
    USER ||--o{ AUDIT_EVENT : performs

    ORGANIZATION {
        uuid id PK
        string name
        string status
    }
    USER {
        uuid id PK
        string identity_reference
    }
    MEMBERSHIP {
        uuid id PK
        uuid organization_id FK
        uuid user_id FK
        string role
    }
    SERVICE {
        uuid id PK
        uuid organization_id FK
        string name
        string status
    }
    SERVICE_DEPENDENCY {
        uuid id PK
        uuid source_service_id FK
        uuid target_service_id FK
        string dependency_type
    }
    INCIDENT {
        uuid id PK
        uuid organization_id FK
        uuid service_id FK
        string severity
        string status
        datetime opened_at
    }
    EVENT {
        uuid id PK
        uuid organization_id FK
        uuid incident_id FK
        string source
        string fingerprint
        datetime occurred_at
    }
    INVESTIGATION {
        uuid id PK
        uuid incident_id FK
        string status
        string model_version
        string prompt_version
    }
    HYPOTHESIS {
        uuid id PK
        uuid investigation_id FK
        string title
        string status
        string confidence_label
    }
    HYPOTHESIS_FEEDBACK {
        uuid id PK
        uuid hypothesis_id FK
        uuid user_id FK
        string decision
        string comment
    }
    KNOWLEDGE_DOCUMENT {
        uuid id PK
        uuid organization_id FK
        string source_type
        string status
    }
    DOCUMENT_CHUNK {
        uuid id PK
        uuid document_id FK
        int ordinal
        vector embedding
    }
    EVIDENCE_REFERENCE {
        uuid id PK
        uuid investigation_id FK
        uuid chunk_id FK
        string source_locator
    }
    POSTMORTEM {
        uuid id PK
        uuid incident_id FK
        string status
        datetime updated_at
    }
    AUDIT_EVENT {
        uuid id PK
        uuid organization_id FK
        uuid actor_id FK
        string action
        datetime occurred_at
    }
```

## Design constraints to verify during implementation

- Every tenant-owned record and query must enforce organization/tenant scope, including Celery tasks and vector retrieval.
- Event ingestion should support an idempotency key or deterministic fingerprint to prevent duplicate processing.
- Evidence references must resolve to stored source material that the current user is authorized to access.
- Hypotheses are not confirmed root causes; reviewer feedback should be recorded.
- The exact identity model may use Django's configured user model rather than a literal `USER` table.
- Vector type, extension, dimensions, indexes, deletion behavior, and document versioning must come from actual migrations.
- Relationship cardinalities are a conceptual baseline; validate them against actual business rules and model constraints.
