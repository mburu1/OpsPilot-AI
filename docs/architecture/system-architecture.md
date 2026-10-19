# System Architecture

## High-Level Overview
OpsPilot AI is an AI-driven operational intelligence platform designed to correlate events, investigate incidents, and provide actionable insights using LLMs.

```mermaid
graph TD
    User((User/SRE)) -->|HTTPS/REST| Gateway[API Gateway/Nginx]
    Gateway -->|Auth/Route| Backend[Django Backend]
    Backend -->|Query/Store| DB[(PostgreSQL)]
    Backend -->|Task Queue| Celery[Celery Worker]
    Celery -->|Event Stream| Redis[(Redis)]
    
    subgraph AI_Engine [AI Intelligence Layer]
        Celery --> AI_Pipeline[AI Pipelines]
        AI_Pipeline --> Embeddings[Embedding Model]
        AI_Pipeline --> LLM[LLM Provider - Claude/GPT]
        AI_Pipeline --> VectorDB[(Vector Database)]
    end
    
    subgraph Data_Sources [External Integrations]
        LogSources[Log Sources] -->|Webhooks/Poll| Backend
        MetricSources[Metric Sources] -->|API| Backend
        EventSources[Event Sources] -->|Stream| Backend
    end
```
