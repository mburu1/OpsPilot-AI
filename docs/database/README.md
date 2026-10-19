# Database Documentation

This directory describes the proposed persistence model for OpsPilot AI. The repository README says application source code was not present when architecture documentation was added; these documents are design guidance, not evidence that models, migrations, indexes, or operational jobs already exist.

## Documents
- [Entity relationship diagram](erd.md)
- [Schema design and data dictionary](schema-design.md)
- [Django migrations and seed data](migrations.md)
- [Security, tenancy, and retention](security-tenancy-retention.md)

## Database baseline
- Primary relational store: PostgreSQL.
- ORM and schema migrations: Django ORM and Django migrations.
- Vector retrieval: PostgreSQL with pgvector, subject to validation of the selected embedding and retrieval design.
- Background processing: Celery with Redis. Redis is not the system of record.

## Design invariants
1. Tenant-owned records must be scoped to an organization and authorized in every request and background task.
2. Foreign keys and database constraints should enforce data integrity wherever practical.
3. Incident and investigation evidence must remain traceable to source events and documents.
4. AI hypotheses are not confirmed root causes without supporting evidence and review.
5. Store timezone-aware timestamps and use UTC consistently at system boundaries.
6. Never store secrets or raw access tokens in ordinary records or logs.
7. Deliver schema changes through reviewed migrations, not manual production SQL.

## Implementation checklist
- [ ] Define concrete Django models and explicit deletion behavior.
- [ ] Add organization-scoped query and authorization tests.
- [ ] Enable required PostgreSQL extensions through controlled procedures.
- [ ] Review generated migrations before applying them.
- [ ] Add indexes based on measured query patterns.
- [ ] Establish backup, restore, retention, and recovery objectives.
- [ ] Derive the ERD from implemented models once available.
