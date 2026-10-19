# Component Diagram

Structural breakdown of the OpsPilot AI system components.

```mermaid
componentDiagram
    package "Frontend" {
        [React SPA] as UI
        [State Manager] as State
    }
    package "Backend" {
        [API Layer] as API
        [Business Logic] as Logic
        [Auth Service] as Auth
    }
    package "AI Layer" {
        [RAG Orchestrator] as RAG
        [Embedding Engine] as Embed
        [LLM Wrapper] as LLM
    }
    database "Storage" {
        [PostgreSQL] as SQL
        [Vector DB] as VDB
        [Redis Cache] as Cache
    }

    UI --> API : REST/WS
    API --> Auth : Validate
    API --> Logic : Process
    Logic --> RAG : Request Analysis
    RAG --> Embed : Vectorize
    RAG --> LLM : Generate
    Logic --> SQL : Persist
    RAG --> VDB : Retrieve
    Logic --> Cache : Fast Access
```
