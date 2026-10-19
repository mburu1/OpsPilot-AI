# OpsPilot AI — Architecture as Code

> **Documentation status:** derived from the attached project README/specification, not verified against application source code. The repository was empty when this documentation was prepared. Treat the diagrams, entity model, API routes, and deployment topology below as the intended design baseline until implementation is pushed and reconciled.

## System context

```mermaid
flowchart LR
    Engineer[Engineer / SRE]
    Sources[Monitoring, logs, deployment events]
    Docs[Runbooks, service docs, past postmortems]
    UI[React + TypeScript incident console]
    API[Django + Django REST Framework]
    DB[(PostgreSQL + pgvector)]
    Redis[(Redis)]
    Workers[Celery workers]
    AI[Provider-neutral LLM and embedding adapters]
    Engineer --> UI
    Sources -->|event ingestion| API
    Docs -->|knowledge ingestion| API
    UI <-->|HTTPS REST| API
    UI <-->|authenticated WebSocket| API
    API --> DB
    API --> Redis
    API -->|enqueue asynchronous work| Workers
    Workers --> DB
    Workers --> Redis
    Workers --> AI
    Workers -->|retrieve and store vectors| DB
    API -->|authorized live updates via Channels| UI
```

## Container and logical architecture

This is a **modular monolith**, not a microservice topology. Domain modules are logical boundaries within Django; Celery workers are independently scalable processes.

```mermaid
flowchart TB
    subgraph Client["Presentation"]
        React["React + TypeScript + Vite"]
    end
    subgraph App["Application boundary"]
        Django["Django / DRF API"]
        Channels["Django Channels / ASGI"]
        Auth["Authentication, authorization, tenant isolation"]
        Modules["Domain modules"]
        Incidents["Incidents and lifecycle"]
        Events["Event ingestion, normalization, correlation"]
        Services["Service inventory and dependency mapping"]
        Knowledge["Knowledge documents and retrieval"]
        Investigations["AI investigations and evidence validation"]
        Reports["Postmortems and reliability analytics"]
        Audit["Audit history"]
    end
    subgraph Async["Asynchronous processing"]
        Celery["Celery workers"]
        Queue["Redis broker / task coordination"]
        Tasks["Event correlation · indexing · embeddings · AI analysis · reports"]
    end
    subgraph Data["Persistence"]
        PG[("PostgreSQL")]
        Vector[("pgvector extension")]
        Cache[("Redis cache / Channels layer")]
    end
    subgraph Providers["External / configurable providers"]
        LLM["LLM provider adapter"]
        Embed["Embedding provider adapter"]
        Inputs["Monitoring and deployment sources"]
    end
    React <-->|REST| Django
    React <-->|WebSocket| Channels
    Django --> Auth
    Channels --> Auth
    Django --> Modules
    Modules --> Incidents
    Modules --> Events
    Modules --> Services
    Modules --> Knowledge
    Modules --> Investigations
    Modules --> Reports
    Modules --> Audit
    Inputs --> Django
    Django --> PG
    Knowledge --> Vector
    PG --- Vector
    Django --> Queue
    Queue --> Celery
    Celery --> Tasks
    Tasks --> PG
    Tasks --> Cache
    Tasks --> LLM
    Tasks --> Embed
    Channels --> Cache
```

## Event ingestion and correlation

```mermaid
sequenceDiagram
    autonumber
    participant Source as Monitoring / deployment source
    participant API as Django API
    participant DB as PostgreSQL
    participant Queue as Redis task queue
    participant Worker as Celery worker
    participant Channel as Django Channels
    participant UI as React incident console

    Source->>API: Submit event with idempotency key
    API->>API: Authenticate, authorize, validate, normalize
    API->>DB: Persist event / deduplication fingerprint
    DB-->>API: Commit result
    API-->>Source: Acknowledge accepted event
    API->>Queue: Enqueue correlation work
    Queue->>Worker: Deliver task
    Worker->>DB: Match existing incident or create incident
    Worker->>DB: Persist event-to-incident relationship and audit data
    Worker->>Channel: Publish minimal authorized update
    Channel-->>UI: Incident changed notification
    UI->>API: Fetch authoritative incident/timeline
    API-->>UI: Tenant-scoped incident representation
```

**Reliability note:** the specification recommends idempotency and reliable database-to-queue delivery (preferably a transactional outbox). The diagram shows the logical workflow; it does not assert that an outbox or particular queue-delivery guarantee is already implemented.

## Evidence-grounded AI investigation (RAG)

```mermaid
sequenceDiagram
    autonumber
    actor Engineer
    participant API as Django API
    participant DB as PostgreSQL + pgvector
    participant Queue as Redis / Celery
    participant Worker as Investigation worker
    participant Retriever as Tenant-scoped retriever
    participant Model as LLM adapter
    participant UI as React console

    Engineer->>API: Request investigation for incident
    API->>DB: Check tenant access and persist investigation job
    API->>Queue: Enqueue investigation
    API-->>Engineer: Accepted, return job identifier

    Queue->>Worker: Run investigation task
    Worker->>DB: Load incident context and permitted evidence
    Worker->>Retriever: Search runbooks, prior incidents, service docs
    Retriever->>DB: Hybrid search with tenant/service filters
    DB-->>Retriever: Relevant authorized passages + source metadata
    Retriever-->>Worker: Evidence set
    Worker->>Model: Request schema-constrained hypotheses and evidence IDs
    Model-->>Worker: Structured hypotheses, uncertainty, recommended checks
    Worker->>Worker: Validate schema, citation IDs, access and evidence links
    Worker->>DB: Save result, model/prompt metadata and audit record
    Worker->>UI: Publish minimal completion notification via Channels
    UI->>API: Fetch investigation result
    API->>DB: Recheck tenant authorization
    DB-->>API: Saved analysis and evidence references
    API-->>UI: Evidence-linked hypotheses marked unconfirmed
    Engineer->>API: Accept, reject or correct hypothesis
    API->>DB: Save reviewer feedback and audit history
```

Rules: retrieved evidence must be authorized for the requesting tenant; citations must resolve to actual stored evidence; vector similarity is not a probability of correctness; hypotheses remain unconfirmed until human review; production remediation is not automatically executed.

## Incident lifecycle (conceptual)

```mermaid
stateDiagram-v2
    [*] --> Open: correlated event creates incident
    Open --> Acknowledged: engineer acknowledges
    Acknowledged --> Investigating: investigation begins
    Investigating --> Mitigating: mitigation work recorded
    Mitigating --> Monitoring: service recovery being verified
    Monitoring --> Resolved: recovery confirmed
    Resolved --> Closed: review / closure complete
    Investigating --> Open: new evidence reopens triage
    Monitoring --> Investigating: symptoms recur
    Resolved --> Investigating: incident reopened
```

These state names are a proposed lifecycle derived from the workflow described in the specification. They must be reconciled with the actual Django model choices and transition rules once source code is available.

## Documentation map

- [Architecture decisions](decisions/README.md)
- [Conceptual ERD](../database/erd.md)
- [Proposed API contract](../api/contract.md)
- [Deployment topology](deployment.md)

## Source of truth and maintenance

1. Update diagrams in the same pull request as relevant domain, API, schema, task, or deployment changes.
2. Generate the production OpenAPI schema from DRF endpoints when available; do not let the proposed API document become an independent competing contract.
3. Replace the conceptual ERD with a schema derived from Django models and migrations.
4. Verify deployment nodes against the checked-in Docker Compose and CI files.
5. Keep proposed elements labeled until confirmed by code and tests.
