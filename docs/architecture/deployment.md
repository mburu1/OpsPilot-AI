# OpsPilot AI Deployment Topology

> **Proposed topology from the attached specification.** The remote repository was empty when this file was authored, so the actual Docker Compose services, ports, health checks, environment variables, and CI workflow could not be verified.

## Logical deployment diagram

```mermaid
flowchart TB
    Browser["Engineer browser"]
    subgraph Compose["Docker Compose development environment (target)"]
        Frontend["React + Vite frontend"]
        Web["Django ASGI web process<br/>DRF + Channels"]
        Worker["Celery worker process(es)"]
        Scheduler["Optional Celery Beat<br/>only if scheduled tasks are needed"]
        Redis[("Redis<br/>broker / cache / channel layer")]
        DB[("PostgreSQL + pgvector")]
    end
    Provider["Configured LLM / embedding provider"]
    Source["Monitoring and deployment event sources"]

    Browser -->|HTTP(S)| Frontend
    Frontend -->|REST / WebSocket| Web
    Source -->|Authenticated event ingestion| Web
    Web -->|Transactions| DB
    Web -->|Queue tasks / channel messages| Redis
    Redis -->|Tasks| Worker
    Worker -->|Read/write| DB
    Worker -->|Task coordination| Redis
    Worker -->|Model requests| Provider
    Scheduler -.->|Scheduled tasks if configured| Redis
```

## Deployment responsibilities

| Process/service | Responsibility | Status in this document |
|---|---|---|
| React/Vite | Browser UI and development asset serving | Target stack from specification |
| Django ASGI | REST API, authentication, domain workflows, WebSocket entry point | Target stack from specification |
| Celery worker | Event processing, indexing, AI investigation, report generation | Target stack from specification |
| PostgreSQL + pgvector | Transactional records and embedding retrieval | Target stack from specification |
| Redis | Celery coordination, cache, Channels layer | Target stack from specification |
| LLM/embedding provider | Configurable external or local model integration | Adapter design specified; providers unverified |
| Celery Beat | Periodic scheduling | Optional; not required by the supplied README |

## Production hardening checklist

- Keep secrets in environment variables or a secret manager; commit only safe example configuration.
- Use separate development, test, and production settings.
- Configure database backups and test restoration.
- Apply migrations as a controlled release step.
- Add readiness/liveness checks and bounded shutdown behavior.
- Configure worker concurrency, retry limits, timeouts, and dead-letter/failure handling appropriate to the broker setup.
- Protect WebSocket endpoints and enforce tenant-scoped subscriptions.
- Collect structured logs, traces, metrics, and queue health indicators.
- Document deployment rollback and provider-outage behavior.
- Validate all service names, ports, health checks, volumes, and dependencies against the eventual checked-in Compose file.
