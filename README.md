# OpsPilot AI — Intelligent Incident Investigation Platform

**Evidence-grounded AI for incident response and service reliability.**

OpsPilot AI is a proposed full-stack incident intelligence platform for correlating operational events, investigating service failures, retrieving engineering knowledge, and producing structured post-incident reports.

> **Repository status:** Architecture documentation is based on the project specification. Application source code was not present in the repository when this README was added. The diagrams, ERD, API routes, and deployment topology are design proposals, not claims that these features have been implemented or tested.

## Intended technology stack

- **Backend:** Python, Django, Django REST Framework
- **Frontend:** React, TypeScript, Vite
- **Data:** PostgreSQL with pgvector
- **Background processing and coordination:** Celery and Redis
- **Real-time updates:** Django Channels and ASGI
- **AI:** provider adapters, embeddings, RAG, structured outputs, evidence validation
- **Testing:** pytest, pytest-django, React Testing Library, Playwright
- **Infrastructure target:** Docker Compose and GitHub Actions

## Architecture documentation

- [System architecture and Mermaid diagrams](docs/architecture/system-architecture.md)
- [Architecture decision records](docs/architecture/decisions/README.md)
- [Conceptual ERD](docs/database/erd.md)
- [Proposed API contract](docs/api/contract.md)
- [Proposed deployment topology](docs/architecture/deployment.md)

## Design principles

1. Evidence must be traceable to its source.
2. AI-generated hypotheses are not confirmed root causes.
3. Tenant isolation applies to APIs, background jobs, and retrieval.
4. Long-running work runs asynchronously.
5. AI quality is evaluated against a versioned benchmark.
6. Production changes require explicit authorization and human approval.
7. Architecture documents must be reconciled with source code as implementation evolves.

## Important status distinction

The attached specification describes the intended architecture and a staged development roadmap. It does not, by itself, prove that the corresponding Django models, routes, Celery tasks, React screens, tests, or Compose services exist. Replace conceptual artifacts with code-derived artifacts when implementation is available. In particular, generate OpenAPI from implemented DRF routes and derive the ERD from Django models and migrations.

## License

No license file was present when this README was created. Add a license before communicating reuse permissions.
