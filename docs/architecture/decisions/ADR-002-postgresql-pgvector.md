# ADR-002: PostgreSQL and pgvector for transactional data and semantic retrieval

- **Status:** Specified by README; implementation unverified
- **Date:** 2026-10-19

## Context

The platform needs authoritative records for tenants, services, incidents, events, audit history, knowledge documents, investigations, and reviewer feedback. It also needs semantic retrieval over runbooks and previous incident reports.

## Decision

Use PostgreSQL as the authoritative relational store and pgvector for embedding storage and similarity retrieval. Keep tenant and service filters part of retrieval authorization, not merely ranking preferences.

## Consequences

- Relational integrity and transactional updates can support incident workflows.
- Vector search can run alongside relational data, reducing the need for a separate vector database in the initial architecture.
- Migrations must manage the pgvector extension and vector indexes explicitly.
- Retrieval must apply tenant authorization and source permissions before evidence is shown to an LLM or user.
- Index choices and retrieval quality must be measured against a versioned benchmark.

## Verification required

Check installed PostgreSQL/pgvector dependencies, Django database settings, migrations, vector fields/indexes, and retrieval queries. This ADR does not claim those components have already been implemented.
