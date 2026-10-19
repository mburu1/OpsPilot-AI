# OpsPilot AI — Intelligent Incident Investigation Platform

**Evidence-grounded AI for incident response and service reliability.**

OpsPilot AI is a full-stack incident intelligence platform that helps software engineering and IT operations teams correlate operational events, investigate service failures, retrieve relevant engineering knowledge, and produce structured post-incident reports.

Rather than treating AI as a standalone chatbot, OpsPilot integrates retrieval-augmented generation (RAG), event processing, evidence validation, human review, and real-time collaboration into an operational workflow.

## The Problem

Production incidents often require engineers to correlate application errors, deployment history, service dependencies, monitoring events, runbooks, and previous incidents. Fragmented evidence and repetitive investigations increase the time needed to diagnose and recover from failures.

OpsPilot AI provides a centralized workflow for turning operational signals into traceable investigations.

## Core Features

- Event ingestion, normalization, deduplication, and correlation.
- Incident lifecycle management and real-time collaboration.
- Service dependency mapping and impact analysis.
- Retrieval-augmented generation using PostgreSQL and pgvector.
- AI-generated root-cause hypotheses linked to supporting evidence.
- Human review and feedback on AI-generated hypotheses.
- Editable postmortems and reliability analytics.
- Tenant-aware authorization, audit history, and operational observability.

## Technology Stack

- Backend: Python, Django, Django REST Framework.
- Frontend: React, TypeScript, Vite.
- Database: PostgreSQL and pgvector.
- Background processing: Celery and Redis.
- Real-time communication: Django Channels and ASGI.
- AI: provider adapters, embeddings, RAG, and structured model outputs.
- Testing: pytest, pytest-django, React Testing Library, and Playwright.
- Infrastructure: Docker Compose and GitHub Actions.

## Architecture

OpsPilot uses a modular monolith with independently scalable background workers. Django owns the domain and transactional workflows; Celery handles event processing, document indexing, and AI investigations. PostgreSQL stores authoritative records and vector embeddings, while Channels delivers authorized real-time updates.

## Engineering Principles

1. Evidence must be traceable to its source.
2. AI-generated hypotheses are not confirmed root causes.
3. Tenant isolation is enforced across APIs, background jobs, and retrieval.
4. Long-running tasks execute asynchronously.
5. AI quality is evaluated against a versioned benchmark.
6. Production changes require explicit authorization and human approval.

## Project Status

Development roadmap: foundation → incident lifecycle → event processing → RAG → AI investigation → reporting → production hardening.

This repository is intended to demonstrate practical full-stack engineering, AI integration, software architecture, testing, and operational reliability. Performance and evaluation results will be published only after they have been measured and reproduced.

## Documentation

- `docs/architecture/` — system design and architecture decisions.
- `docs/ooad/` — requirements, use cases, and domain model.
- `docs/uml/` — sequence, component, activity, and deployment diagrams.
- `docs/database/` — ERD, schema design, and indexing.
- `docs/api/` — API conventions and OpenAPI.
- `docs/ai/` — RAG, evaluation, providers, and AI safety.
- `docs/security/` — authentication, authorization, and threat modeling.
- `docs/testing/` — test strategy and acceptance criteria.
- `docs/deployment/` — setup, release, monitoring, and recovery.

## Responsible AI

OpsPilot AI supports engineers; it does not replace operational judgment. Generated recommendations require verification, evidence is validated before display, and production remediation is not automatically executed.

## License

See `LICENSE`.


GitHub Portfolio Project: AI-Powered Incident Intelligence & Reliability Platform
For this job description, I would build a production-oriented application that solves a real operational problem, demonstrates deep Python/Django skills, and uses AI as part of the actual business workflow rather than simply adding a chatbot.

My recommendation is OpsPilot AI — an AI-assisted incident investigation, root-cause analysis, and service reliability platform for software engineering and IT operations teams.

It is designed to demonstrate the exact combination this employer wants: Django, React, PostgreSQL, vector search, LLM integration, REST APIs, WebSockets, testing, performance engineering, and technical ownership.







incop.ai


Python + Django
React + TypeScript
AI + RAG
PostgreSQL + pgvector
WebSockets


1. The real-world problem
When an online platform experiences a production incident, engineers often have to investigate information scattered across application logs, monitoring dashboards, deployment histories, API errors, internal runbooks, and previous incidents.

This leads to several problems:
- Engineers spend too much time correlating events across different systems.
- Similar incidents get investigated repeatedly because past resolutions are difficult to find.
- Alerts do not always explain the likely impact or what to investigate first.
- Teams may use AI assistants that generate plausible but unsupported root-cause explanations.
- Incident reports and post-incident reviews consume valuable engineering time.
OpsPilot AI brings these workflows together. It ingests operational events, correlates related failures, retrieves relevant engineering knowledge, proposes evidence-backed hypotheses, and helps engineers coordinate and resolve incidents.

The platform must distinguish between a confirmed root cause and an AI-generated hypothesis. It should never claim to have fixed a production problem merely because an LLM suggested a solution.
2. What makes this a serious engineering project?









1. Intelligent incident correlation

Ingest errors, alerts, deployments and service-health events. Group related signals into incidents using service identity, timestamps, fingerprints and configurable correlation rules.












2. Evidence-grounded AI investigation

Use RAG to retrieve relevant runbooks, previous incident reports and service documentation. Produce ranked root-cause hypotheses with source citations and supporting evidence.












3. Service dependency and impact analysis

Represent dependencies between services and identify which upstream or downstream systems may be affected by an incident.












4. Live incident response

Stream incident updates to React clients through WebSockets. Support assignment, severity changes, investigation notes, action tracking and incident timelines.












5. Automated post-incident analysis

Generate editable incident timelines, impact summaries, contributing factors and follow-up recommendations, with links to supporting evidence.



This is not a CRUD application with an AI chat window. The AI features depend on real data pipelines, retrieval, evidence evaluation and operational workflows. The non-AI components remain useful if the LLM provider is unavailable.
3. Technology stack
Use a Python-first backend because Python and Django are central requirements of the role. Keep the frontend in React and TypeScript to demonstrate full-stack ownership.
Layer	Technology	Purpose
Backend	Python, Django, Django REST Framework	Business logic, authentication, APIs and domain workflows
Real-time	Django Channels, ASGI	Live incident updates and collaborative response
Frontend	React, TypeScript, Vite	Incident console, investigation views and analytics
Relational database	PostgreSQL	Tenants, services, incidents, events, audit history
Vector search	pgvector	Semantic retrieval of runbooks and past incidents
Cache / messaging	Redis	Caching, WebSocket channel layer and task coordination
Background workers	Celery	Event ingestion, embeddings, correlation and AI jobs
AI	Provider-neutral LLM adapter	Root-cause hypotheses, summarization and incident reports
AI orchestration	LangChain or LlamaIndex, selectively	Retrieval and document-processing workflows
Validation	Pydantic	Structured AI outputs and ingestion payload validation
Testing	pytest, pytest-django, React Testing Library, Playwright	Unit, integration, frontend and end-to-end tests
API documentation	OpenAPI	Contract-first API documentation
Infrastructure	Docker Compose, GitHub Actions	Reproducible development and continuous integration
Observability	OpenTelemetry, structured logs, Prometheus-compatible metrics	Performance, tracing and operational diagnostics
Django supports ASGI-based asynchronous request handling, while Django Channels extends Django to WebSocket and other protocols. Those capabilities make this stack appropriate for a live incident console. 

Django
+1




For AI, use an adapter so you can switch between OpenAI, Anthropic and a local model without changing your domain logic. Use schema-constrained outputs and evaluate retrieval and generation separately; structured output alone does not guarantee that an explanation is factually correct. 

OpenAI API
+2




Architecture decision: begin with a modular monolith and independently scalable workers. Do not start with a large collection of microservices; prove the domain boundaries and workload first.
4. System architecture
Create the following architecture document as docs/architecture/system-architecture.md.
React + TypeScript

Incident console · Service map · Investigation workspace · Analytics

HTTPS / REST / WebSocket

Django API + Channels

Authentication · Authorization · Tenant isolation · API validation


Domain modules

Incidents, events, services, knowledge, audit and reporting


AI pipeline

Retrieval, evidence, hypotheses, evaluations and reports




PostgreSQL

Transactional records


pgvector

Semantic retrieval


Redis

Cache and channels




Celery workers

Event processing · Correlation · Document indexing · AI analysis · Report generation


The diagram shows logical responsibilities, not separate microservices. The Django application owns business rules; Celery executes slow or retryable work outside the request-response path.
Request and event lifecycle
#chatgpt-mermaid-_r_16p_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-_r_16p_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_16p_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_16p_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-_r_16p_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-_r_16p_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-_r_16p_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-_r_16p_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-_r_16p_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-_r_16p_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-_r_16p_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-_r_16p_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_16p_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_16p_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-_r_16p_ p{margin:0;}#chatgpt-mermaid-_r_16p_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_16p_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_16p_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_16p_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-_r_16p_ .label text,#chatgpt-mermaid-_r_16p_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_16p_ .node rect,#chatgpt-mermaid-_r_16p_ .node circle,#chatgpt-mermaid-_r_16p_ .node ellipse,#chatgpt-mermaid-_r_16p_ .node polygon,#chatgpt-mermaid-_r_16p_ .node path{fill:rgb(17, 40, 19);stroke:rgb(58, 132, 63);stroke-width:1px;}#chatgpt-mermaid-_r_16p_ .rough-node .label text,#chatgpt-mermaid-_r_16p_ .node .label text,#chatgpt-mermaid-_r_16p_ .image-shape .label,#chatgpt-mermaid-_r_16p_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-_r_16p_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-_r_16p_ .rough-node .label,#chatgpt-mermaid-_r_16p_ .node .label,#chatgpt-mermaid-_r_16p_ .image-shape .label,#chatgpt-mermaid-_r_16p_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-_r_16p_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-_r_16p_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_16p_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-_r_16p_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-_r_16p_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-_r_16p_ .edgeLabel{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-_r_16p_ .edgeLabel p{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-_r_16p_ .edgeLabel rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_16p_ .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#chatgpt-mermaid-_r_16p_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-_r_16p_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_16p_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_16p_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-_r_16p_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_16p_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-_r_16p_ .icon-shape,#chatgpt-mermaid-_r_16p_ .image-shape{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-_r_16p_ .icon-shape p,#chatgpt-mermaid-_r_16p_ .image-shape p{background-color:rgb(0, 0, 0);padding:2px;}#chatgpt-mermaid-_r_16p_ .icon-shape .label rect,#chatgpt-mermaid-_r_16p_ .image-shape .label rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_16p_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-_r_16p_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-_r_16p_ .node .neo-node{stroke:rgb(58, 132, 63);}#chatgpt-mermaid-_r_16p_ [data-look="neo"].node rect,#chatgpt-mermaid-_r_16p_ [data-look="neo"].cluster rect,#chatgpt-mermaid-_r_16p_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-_r_16p_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_16p_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-_r_16p_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-_r_16p_-gradient);stroke-width:1px;}#chatgpt-mermaid-_r_16p_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_16p_ [data-look="neo"].node .neo-line path{stroke:rgb(58, 132, 63);filter:none;}#chatgpt-mermaid-_r_16p_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-_r_16p_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_16p_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-_r_16p_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-_r_16p_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_16p_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-_r_16p_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_16p_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(140, 223, 173);}#chatgpt-mermaid-_r_16p_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(140, 223, 173);}#chatgpt-mermaid-_r_16p_ .node tspan[font-weight="normal"],#chatgpt-mermaid-_r_16p_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-_r_16p_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(2, 28, 12);stroke:rgb(26, 75, 45);stroke-width:1px;}#chatgpt-mermaid-_r_16p_ .node rect,#chatgpt-mermaid-_r_16p_ .node circle,#chatgpt-mermaid-_r_16p_ .node ellipse,#chatgpt-mermaid-_r_16p_ .node polygon,#chatgpt-mermaid-_r_16p_ .node path{fill:rgb(0, 55, 22);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-_r_16p_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-_r_16p_ .node.mermaid-decision .label-container{fill:rgb(2, 28, 12);stroke:rgb(26, 75, 45);stroke-dasharray:2,2;}#chatgpt-mermaid-_r_16p_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-_r_16p_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_16p_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}Monitoring event or manualreportValidate and authenticateNormalize and deduplicatePersist eventQueue correlation taskMatch or create incidentPublish incident updateReact console via WebSocketQueue AI investigationRetrieve relevant runbooks andpast incidentsGenerate structuredhypothesesValidate citations and evidenceSave analysis and audit recordNotify connected clientsEngineer reviews and confirmsor rejects





Important implementation details:
- Persist an event before acknowledging successful ingestion.
- Use idempotency keys or deterministic fingerprints to prevent duplicate incidents.
- Dispatch work reliably, preferably using a transactional outbox for database-to-queue delivery.
- Retry transient provider failures with bounded backoff; move repeatedly failing jobs to a dead-letter or failed-task workflow.
- Store AI analysis versions so an engineer can compare results after a prompt, model or retrieval change.
- Require human approval for remediation actions. The initial release should recommend actions, not execute production changes.
5. GitHub repository structure
Use a repository named opspilot-ai. Keep the backend organized by business capability rather than creating a folder for every technical abstraction without a clear purpose.
opspilot-ai/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── .editorconfig
├── .gitignore
├── .env.example
├── Makefile
├── compose.yaml
├── pyproject.toml
├── package.json
│
├── backend/
│   ├── manage.py
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   ├── test.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   ├── wsgi.py
│   │   └── celery.py
│   │
│   ├── apps/
│   │   ├── organizations/
│   │   ├── accounts/
│   │   ├── services/
│   │   ├── events/
│   │   ├── incidents/
│   │   ├── correlations/
│   │   ├── knowledge/
│   │   ├── ai_investigations/
│   │   ├── reports/
│   │   ├── notifications/
│   │   ├── audit/
│   │   └── integrations/
│   │
│   ├── platform/
│   │   ├── authentication/
│   │   ├── permissions/
│   │   ├── exceptions/
│   │   ├── logging/
│   │   ├── pagination/
│   │   ├── idempotency/
│   │   └── observability/
│   │
│   └── tests/
│       ├── unit/
│       ├── integration/
│       ├── api/
│       ├── security/
│       └── performance/
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── features/
│   │   │   ├── incidents/
│   │   │   ├── investigations/
│   │   │   ├── services/
│   │   │   ├── knowledge/
│   │   │   ├── analytics/
│   │   │   └── settings/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── api/
│   │   ├── routes/
│   │   ├── types/
│   │   └── styles/
│   └── tests/
│       ├── unit/
│       ├── components/
│       └── e2e/
│
├── ai/
│   ├── providers/
│   ├── embeddings/
│   ├── retrieval/
│   ├── pipelines/
│   ├── prompts/
│   ├── schemas/
│   ├── evaluation/
│   └── datasets/
│
├── integrations/
│   ├── webhook_examples/
│   ├── synthetic_event_generator/
│   └── sample_log_fixtures/
│
├── infrastructure/
│   ├── docker/
│   ├── postgres/
│   ├── monitoring/
│   └── scripts/
│
├── docs/
│   ├── architecture/
│   │   ├── system-architecture.md
│   │   ├── architecture-decisions.md
│   │   ├── dependency-rules.md
│   │   └── scalability.md
│   ├── ooad/
│   │   ├── requirements.md
│   │   ├── use-cases.md
│   │   ├── domain-model.md
│   │   └── class-diagram.md
│   ├── uml/
│   │   ├── component-diagram.md
│   │   ├── sequence-diagrams.md
│   │   ├── activity-diagrams.md
│   │   └── deployment-diagram.md
│   ├── database/
│   │   ├── erd.md
│   │   ├── schema-design.md
│   │   └── indexing-strategy.md
│   ├── api/
│   │   ├── api-conventions.md
│   │   ├── authentication.md
│   │   └── openapi.md
│   ├── ai/
│   │   ├── rag-pipeline.md
│   │   ├── evaluation-strategy.md
│   │   ├── model-providers.md
│   │   └── safety-and-limitations.md
│   ├── security/
│   ├── testing/
│   ├── deployment/
│   └── adr/
│
└── .github/
    ├── workflows/
    │   ├── backend-ci.yml
    │   ├── frontend-ci.yml
    │   ├── security.yml
    │   └── docker-build.yml
    ├── ISSUE_TEMPLATE/
    └── PULL_REQUEST_TEMPLATE.md


This is the target structure, not a requirement to create every directory on day one. Add each module when its implementation begins.
Backend module responsibilities
Module	Main responsibility
organizations	Tenant ownership, organization settings and isolation
accounts	Users, memberships, roles and invitations
services	Service registry, ownership and dependency relationships
events	Event ingestion, normalization and deduplication
incidents	Incident lifecycle, severity, assignment and timeline
correlations	Deterministic grouping of related events
knowledge	Runbooks, documents, chunks and vector retrieval
ai_investigations	Investigation jobs, hypotheses, evidence and feedback
reports	Incident summaries, postmortems and operational metrics
notifications	WebSocket events and notification delivery
audit	Append-only records of security-sensitive actions
integrations	External monitoring providers and webhook adapters
Each Django app should own its domain models and business rules. Avoid circular imports and cross-app writes that bypass the owning service. Start with ordinary Django services and transactions; introduce more elaborate repository abstractions only where they provide measurable value.
6. Object-oriented analysis and design (OOAD)
Create docs/ooad/requirements.md before implementing the domain models.
Core actors
- Organization administrator: manages users, services, access and integrations.
- Incident commander: coordinates an incident, assignments and response.
- Reliability engineer: investigates evidence and confirms root causes.
- Observer: views authorized incidents and reports.
- External monitoring system: submits events through an authenticated ingestion interface.
- AI analysis worker: retrieves evidence and produces proposed hypotheses.
Core domain entities

Organization and Membership

Tenant boundaries, user roles and access policies.




Service and ServiceDependency

Represent a monitored service and its upstream or downstream dependencies.




Event and Incident

Preserve raw event evidence, normalized attributes and incident lifecycle history.




KnowledgeDocument and DocumentChunk

Versioned runbooks, documentation and embeddings with source metadata.




Investigation, Hypothesis and EvidenceReference

Track analysis versions, proposed causes, confidence indicators and verifiable supporting sources.



Domain rules that make the project credible
1. An event belongs to one organization and cannot be attached to another organization's incident.
2. An incident has a controlled state transition: OPEN → ACKNOWLEDGED → INVESTIGATING → RESOLVED → CLOSED, with explicitly permitted reopening.
3. A duplicate webhook delivery must not create a duplicate event.
4. AI hypotheses must reference retrieved evidence where available and must be labeled as unconfirmed until reviewed.
5. Closing an incident must preserve its timeline, investigation history and audit trail.
6. A document re-indexing operation must not silently expose stale or unauthorized content through vector retrieval.
7. Severity and service-impact changes must be attributable to a user or a named automated process.
7. UML use-case diagram
Save the following as docs/ooad/use-cases.md. GitHub can render Mermaid diagrams directly in Markdown.
#chatgpt-mermaid-_r_17o_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-_r_17o_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_17o_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_17o_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-_r_17o_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-_r_17o_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-_r_17o_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-_r_17o_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-_r_17o_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-_r_17o_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-_r_17o_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-_r_17o_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_17o_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_17o_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-_r_17o_ p{margin:0;}#chatgpt-mermaid-_r_17o_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_17o_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_17o_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_17o_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-_r_17o_ .label text,#chatgpt-mermaid-_r_17o_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_17o_ .node rect,#chatgpt-mermaid-_r_17o_ .node circle,#chatgpt-mermaid-_r_17o_ .node ellipse,#chatgpt-mermaid-_r_17o_ .node polygon,#chatgpt-mermaid-_r_17o_ .node path{fill:rgb(17, 40, 19);stroke:rgb(58, 132, 63);stroke-width:1px;}#chatgpt-mermaid-_r_17o_ .rough-node .label text,#chatgpt-mermaid-_r_17o_ .node .label text,#chatgpt-mermaid-_r_17o_ .image-shape .label,#chatgpt-mermaid-_r_17o_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-_r_17o_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-_r_17o_ .rough-node .label,#chatgpt-mermaid-_r_17o_ .node .label,#chatgpt-mermaid-_r_17o_ .image-shape .label,#chatgpt-mermaid-_r_17o_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-_r_17o_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-_r_17o_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_17o_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-_r_17o_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-_r_17o_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-_r_17o_ .edgeLabel{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-_r_17o_ .edgeLabel p{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-_r_17o_ .edgeLabel rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_17o_ .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#chatgpt-mermaid-_r_17o_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-_r_17o_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_17o_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_17o_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-_r_17o_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_17o_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-_r_17o_ .icon-shape,#chatgpt-mermaid-_r_17o_ .image-shape{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-_r_17o_ .icon-shape p,#chatgpt-mermaid-_r_17o_ .image-shape p{background-color:rgb(0, 0, 0);padding:2px;}#chatgpt-mermaid-_r_17o_ .icon-shape .label rect,#chatgpt-mermaid-_r_17o_ .image-shape .label rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_17o_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-_r_17o_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-_r_17o_ .node .neo-node{stroke:rgb(58, 132, 63);}#chatgpt-mermaid-_r_17o_ [data-look="neo"].node rect,#chatgpt-mermaid-_r_17o_ [data-look="neo"].cluster rect,#chatgpt-mermaid-_r_17o_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-_r_17o_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_17o_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-_r_17o_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-_r_17o_-gradient);stroke-width:1px;}#chatgpt-mermaid-_r_17o_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_17o_ [data-look="neo"].node .neo-line path{stroke:rgb(58, 132, 63);filter:none;}#chatgpt-mermaid-_r_17o_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-_r_17o_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_17o_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-_r_17o_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-_r_17o_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_17o_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-_r_17o_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_17o_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(140, 223, 173);}#chatgpt-mermaid-_r_17o_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(140, 223, 173);}#chatgpt-mermaid-_r_17o_ .node tspan[font-weight="normal"],#chatgpt-mermaid-_r_17o_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-_r_17o_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(2, 28, 12);stroke:rgb(26, 75, 45);stroke-width:1px;}#chatgpt-mermaid-_r_17o_ .node rect,#chatgpt-mermaid-_r_17o_ .node circle,#chatgpt-mermaid-_r_17o_ .node ellipse,#chatgpt-mermaid-_r_17o_ .node polygon,#chatgpt-mermaid-_r_17o_ .node path{fill:rgb(0, 55, 22);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-_r_17o_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-_r_17o_ .node.mermaid-decision .label-container{fill:rgb(2, 28, 12);stroke:rgb(26, 75, 45);stroke-dasharray:2,2;}#chatgpt-mermaid-_r_17o_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-_r_17o_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_17o_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}OpsPilot AIManage services and accessIngest operational eventsCorrelate incident signalsInvestigate with AIReview evidence andhypothesesManage response andassignmentsGenerate postmortemView reliability analyticsOrganization AdminReliability EngineerIncident CommanderMonitoring Integration





8. UML sequence diagram: AI investigation
Save this in docs/uml/sequence-diagrams.md.
WebSocketLLM ProviderRAG ServiceCelery / RedisPostgreSQLDjango APIReact UIWebSocketLLM ProviderRAG ServiceCelery / RedisPostgreSQLDjango APIReact UI#chatgpt-mermaid-_r_181_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-_r_181_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_181_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_181_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-_r_181_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-_r_181_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-_r_181_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-_r_181_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-_r_181_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-_r_181_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-_r_181_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-_r_181_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_181_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_181_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-_r_181_ p{margin:0;}#chatgpt-mermaid-_r_181_ .actor{stroke:rgb(58, 132, 63);fill:rgb(17, 40, 19);stroke-width:1;}#chatgpt-mermaid-_r_181_ rect.actor.outer-path[data-look="neo"]{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_181_ rect.note[data-look="neo"]{stroke:rgb(172, 79, 35);fill:rgb(48, 48, 48);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_181_ text.actor>tspan{fill:rgb(237, 237, 237);stroke:none;}#chatgpt-mermaid-_r_181_ .actor-line{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_181_ .innerArc{stroke-width:1.5;stroke-dasharray:none;}#chatgpt-mermaid-_r_181_ .messageLine0{stroke-width:1.5;stroke-dasharray:none;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_181_ .messageLine1{stroke-width:1.5;stroke-dasharray:2,2;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_181_ [id$="-arrowhead"] path{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_181_ .sequenceNumber{fill:#505050;}#chatgpt-mermaid-_r_181_ [id$="-sequencenumber"]{fill:rgb(175, 175, 175);}#chatgpt-mermaid-_r_181_ [id$="-crosshead"] path{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_181_ .messageText{fill:rgb(237, 237, 237);stroke:none;}#chatgpt-mermaid-_r_181_ .labelBox{stroke:rgba(255, 255, 255, 0.15);fill:rgb(0, 0, 0);filter:none;}#chatgpt-mermaid-_r_181_ .labelText,#chatgpt-mermaid-_r_181_ .labelText>tspan{fill:rgb(237, 237, 237);stroke:none;}#chatgpt-mermaid-_r_181_ .loopText,#chatgpt-mermaid-_r_181_ .loopText>tspan{fill:rgb(237, 237, 237);stroke:none;}#chatgpt-mermaid-_r_181_ .sectionTitle,#chatgpt-mermaid-_r_181_ .sectionTitle>tspan{fill:rgb(237, 237, 237);stroke:none;}#chatgpt-mermaid-_r_181_ .loopLine{stroke-width:2px;stroke-dasharray:2,2;stroke:rgba(255, 255, 255, 0.15);fill:rgba(255, 255, 255, 0.15);}#chatgpt-mermaid-_r_181_ .note{stroke:rgb(172, 79, 35);fill:rgb(48, 48, 48);}#chatgpt-mermaid-_r_181_ .noteText,#chatgpt-mermaid-_r_181_ .noteText>tspan{fill:rgb(237, 237, 237);stroke:none;font-weight:normal;}#chatgpt-mermaid-_r_181_ .activation0{fill:rgb(48, 48, 48);stroke:hsl(0, 0%, 8.8235294118%);}#chatgpt-mermaid-_r_181_ .activation1{fill:rgb(48, 48, 48);stroke:hsl(0, 0%, 8.8235294118%);}#chatgpt-mermaid-_r_181_ .activation2{fill:rgb(48, 48, 48);stroke:hsl(0, 0%, 8.8235294118%);}#chatgpt-mermaid-_r_181_ .actorPopupMenu{position:absolute;}#chatgpt-mermaid-_r_181_ .actorPopupMenuPanel{position:absolute;fill:rgb(17, 40, 19);box-shadow:0px 8px 16px 0px rgba(0,0,0,0.2);filter:drop-shadow(3px 5px 2px rgb(0 0 0 / 0.4));}#chatgpt-mermaid-_r_181_ .actor-man circle,#chatgpt-mermaid-_r_181_ line{fill:rgb(17, 40, 19);stroke-width:2px;}#chatgpt-mermaid-_r_181_ g rect.rect{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));stroke:rgb(58, 132, 63);}#chatgpt-mermaid-_r_181_ .node .neo-node{stroke:rgb(58, 132, 63);}#chatgpt-mermaid-_r_181_ [data-look="neo"].node rect,#chatgpt-mermaid-_r_181_ [data-look="neo"].cluster rect,#chatgpt-mermaid-_r_181_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-_r_181_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_181_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-_r_181_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-_r_181_-gradient);stroke-width:1px;}#chatgpt-mermaid-_r_181_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_181_ [data-look="neo"].node .neo-line path{stroke:rgb(58, 132, 63);filter:none;}#chatgpt-mermaid-_r_181_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-_r_181_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_181_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-_r_181_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-_r_181_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_181_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-_r_181_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_181_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}EngineerRequest investigationPOST /api/v1/incidents/{id}/investigationsVerify access and save jobDispatch after transaction commit202 Accepted + job IDExecute investigationRetrieve incident and authorized evidenceSearch pgvector and apply metadata filtersSubmit bounded evidence and output schemaStructured hypotheses and citationsValidate references and outputSave analysis and evidence referencesPublish analysis-ready eventInvestigation completedDisplay hypotheses and sourcesEngineer





The API should return 202 Accepted for work that continues asynchronously, not hold an HTTP request open while the model processes a large investigation. The UI can display job progress and receive completion events over WebSockets.
9. Database architecture and ERD
Use PostgreSQL as the system of record and pgvector within PostgreSQL for semantic retrieval. You do not need MongoDB in the first release: introducing a second database without a demonstrated document-storage or query requirement would add operational complexity rather than improve the design.

Save this diagram as docs/database/erd.md.
#chatgpt-mermaid-_r_18a_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-_r_18a_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_18a_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_18a_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-_r_18a_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-_r_18a_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-_r_18a_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-_r_18a_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-_r_18a_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-_r_18a_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-_r_18a_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-_r_18a_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_18a_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_18a_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-_r_18a_ p{margin:0;}#chatgpt-mermaid-_r_18a_ .entityBox{fill:rgb(17, 40, 19);stroke:rgb(58, 132, 63);}#chatgpt-mermaid-_r_18a_ .relationshipLabelBox{fill:rgb(48, 48, 48);opacity:0.7;background-color:rgb(48, 48, 48);}#chatgpt-mermaid-_r_18a_ .relationshipLabelBox rect{opacity:0.5;}#chatgpt-mermaid-_r_18a_ .labelBkg{background-color:rgba(48, 48, 48, 0.5);}#chatgpt-mermaid-_r_18a_ .edgeLabel{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-_r_18a_ .edgeLabel .label rect{fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_18a_ .edgeLabel .label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_18a_ .edgeLabel .label{fill:rgb(58, 132, 63);font-size:14px;}#chatgpt-mermaid-_r_18a_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_18a_ .edge-pattern-dashed{stroke-dasharray:8,8;}#chatgpt-mermaid-_r_18a_ .node rect,#chatgpt-mermaid-_r_18a_ .node circle,#chatgpt-mermaid-_r_18a_ .node ellipse,#chatgpt-mermaid-_r_18a_ .node polygon{fill:rgb(17, 40, 19);stroke:rgb(58, 132, 63);stroke-width:1px;}#chatgpt-mermaid-_r_18a_ .relationshipLine{stroke:rgb(175, 175, 175);stroke-width:1px;fill:none;}#chatgpt-mermaid-_r_18a_ .marker{fill:none!important;stroke:rgb(175, 175, 175)!important;stroke-width:1;}#chatgpt-mermaid-_r_18a_ [data-look=neo].labelBkg{background-color:rgba(48, 48, 48, 0.5);}#chatgpt-mermaid-_r_18a_ .node .neo-node{stroke:rgb(58, 132, 63);}#chatgpt-mermaid-_r_18a_ [data-look="neo"].node rect,#chatgpt-mermaid-_r_18a_ [data-look="neo"].cluster rect,#chatgpt-mermaid-_r_18a_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-_r_18a_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_18a_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-_r_18a_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-_r_18a_-gradient);stroke-width:1px;}#chatgpt-mermaid-_r_18a_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_18a_ [data-look="neo"].node .neo-line path{stroke:rgb(58, 132, 63);filter:none;}#chatgpt-mermaid-_r_18a_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-_r_18a_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_18a_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-_r_18a_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-_r_18a_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_18a_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-_r_18a_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_18a_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}ORGANIZATIONuuididPKstringnamedatetimecreated_atMEMBERSHIPuuididPKuuidorganization_idFKuuiduser_idFKstringroleUSERuuididPKstringemailSERVICEuuididPKuuidorganization_idFKstringnamestringenvironmentSERVICE_DEPENDENCYEVENTuuididPKuuidorganization_idFKuuidservice_idFKstringfingerprintdatetimeoccurred_atINCIDENTuuididPKuuidorganization_idFKstringtitlestringseveritystringstatusINCIDENT_EVENTINVESTIGATIONuuididPKuuidincident_idFKstringstatusstringmodel_versionHYPOTHESISuuididPKuuidinvestigation_idFKstringsummarystringreview_statusEVIDENCE_REFERENCEuuididPKuuidhypothesis_idFKuuidchunk_idFKstringevidence_typeKNOWLEDGE_DOCUMENTuuididPKuuidorganization_idFKstringtitlestringversionDOCUMENT_CHUNKuuididPKuuiddocument_idFKintchunk_indexvectorembeddingINCIDENT_TIMELINE_ENTRYAUDIT_ENTRYhasjoinsownsdependsreceivesemitsownscontainslinkedanalyzedproposessupported_bycontainscited_byrecordsaudited





This is a conceptual ERD; refine the physical schema and cardinalities during implementation.
Database rules
- Use UUID primary keys for externally exposed entities.
- Include organization_id on tenant-owned records, with database constraints where practical to prevent cross-tenant relationships.
- Add unique constraints for organization-scoped event idempotency keys.
- Index incident status, severity, creation time and service references.
- Index event fingerprints and timestamps for correlation queries.
- Add pgvector indexes only after selecting the embedding dimensions, distance metric and expected data volume.
- Store document versions and ingestion status so that re-indexing can be retried safely.
- Use Django migrations as the authoritative schema history.
For production, validate tenant isolation in both application queries and database constraints. PostgreSQL row-level security can provide an additional defense, but it must be configured carefully with pooled connections and tenant context.
10. AI architecture: retrieval-augmented generation
Save this as docs/ai/rag-pipeline.md.
#chatgpt-mermaid-_r_18j_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-_r_18j_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_18j_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_18j_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-_r_18j_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-_r_18j_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-_r_18j_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-_r_18j_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-_r_18j_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-_r_18j_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-_r_18j_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-_r_18j_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_18j_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_18j_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-_r_18j_ p{margin:0;}#chatgpt-mermaid-_r_18j_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_18j_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_18j_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_18j_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-_r_18j_ .label text,#chatgpt-mermaid-_r_18j_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_18j_ .node rect,#chatgpt-mermaid-_r_18j_ .node circle,#chatgpt-mermaid-_r_18j_ .node ellipse,#chatgpt-mermaid-_r_18j_ .node polygon,#chatgpt-mermaid-_r_18j_ .node path{fill:rgb(17, 40, 19);stroke:rgb(58, 132, 63);stroke-width:1px;}#chatgpt-mermaid-_r_18j_ .rough-node .label text,#chatgpt-mermaid-_r_18j_ .node .label text,#chatgpt-mermaid-_r_18j_ .image-shape .label,#chatgpt-mermaid-_r_18j_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-_r_18j_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-_r_18j_ .rough-node .label,#chatgpt-mermaid-_r_18j_ .node .label,#chatgpt-mermaid-_r_18j_ .image-shape .label,#chatgpt-mermaid-_r_18j_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-_r_18j_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-_r_18j_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_18j_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-_r_18j_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-_r_18j_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-_r_18j_ .edgeLabel{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-_r_18j_ .edgeLabel p{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-_r_18j_ .edgeLabel rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_18j_ .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#chatgpt-mermaid-_r_18j_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-_r_18j_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_18j_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_18j_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-_r_18j_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_18j_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-_r_18j_ .icon-shape,#chatgpt-mermaid-_r_18j_ .image-shape{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-_r_18j_ .icon-shape p,#chatgpt-mermaid-_r_18j_ .image-shape p{background-color:rgb(0, 0, 0);padding:2px;}#chatgpt-mermaid-_r_18j_ .icon-shape .label rect,#chatgpt-mermaid-_r_18j_ .image-shape .label rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_18j_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-_r_18j_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-_r_18j_ .node .neo-node{stroke:rgb(58, 132, 63);}#chatgpt-mermaid-_r_18j_ [data-look="neo"].node rect,#chatgpt-mermaid-_r_18j_ [data-look="neo"].cluster rect,#chatgpt-mermaid-_r_18j_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-_r_18j_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_18j_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-_r_18j_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-_r_18j_-gradient);stroke-width:1px;}#chatgpt-mermaid-_r_18j_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_18j_ [data-look="neo"].node .neo-line path{stroke:rgb(58, 132, 63);filter:none;}#chatgpt-mermaid-_r_18j_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-_r_18j_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_18j_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-_r_18j_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-_r_18j_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_18j_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-_r_18j_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_18j_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(140, 223, 173);}#chatgpt-mermaid-_r_18j_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(140, 223, 173);}#chatgpt-mermaid-_r_18j_ .node tspan[font-weight="normal"],#chatgpt-mermaid-_r_18j_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-_r_18j_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(2, 28, 12);stroke:rgb(26, 75, 45);stroke-width:1px;}#chatgpt-mermaid-_r_18j_ .node rect,#chatgpt-mermaid-_r_18j_ .node circle,#chatgpt-mermaid-_r_18j_ .node ellipse,#chatgpt-mermaid-_r_18j_ .node polygon,#chatgpt-mermaid-_r_18j_ .node path{fill:rgb(0, 55, 22);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-_r_18j_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-_r_18j_ .node.mermaid-decision .label-container{fill:rgb(2, 28, 12);stroke:rgb(26, 75, 45);stroke-dasharray:2,2;}#chatgpt-mermaid-_r_18j_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-_r_18j_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_18j_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}InvestigationIngestionIncident events and engineerquestionBuild authorized retrievalqueryHybrid retrieval: keywords andvectorsRank and deduplicate evidenceLLM generates structuredhypothesesValidate schema and citedsourcesSave analysis for human reviewRunbooks, incident reports,service docsParse and normalizeChunk and attach metadataGenerate embeddingsStore chunks and vectors inpgvector





AI investigation pipeline
1. Ingest: accept runbooks, prior incident reports, service metadata and approved operational documentation.
2. Normalize: extract text, preserve source identifiers and remove unsupported file formats or unsafe content.
3. Chunk: split documents into manageable overlapping sections while preserving document and section metadata.
4. Embed: generate vectors through the configured embedding provider.
5. Retrieve: combine semantic similarity with keyword search, tenant filters, service context and time constraints.
6. Generate: ask the selected model for a constrained response containing hypotheses, evidence IDs, uncertainties and suggested investigation steps.
7. Validate: ensure citations reference retrieved, authorized evidence; reject malformed or fabricated references.
8. Evaluate: compare retrieval quality and hypothesis quality against a versioned benchmark dataset.
9. Review: let engineers accept, reject or correct hypotheses and capture feedback.
A key distinction is that similarity scores are not probabilities of root-cause correctness. Do not display a raw vector similarity score as if it were the probability that a hypothesis is true.
Example structured AI output
{
  "incident_summary": "Elevated checkout API latency after deployment.",
  "hypotheses": [
    {
      "title": "Database connection pool exhaustion",
      "explanation": "Connection acquisition time increased after deployment.",
      "evidence_ids": [
        "evidence-001",
        "evidence-004"
      ],
      "confidence": "medium",
      "status": "unconfirmed"
    }
  ],
  "missing_evidence": [
    "Database connection pool utilization"
  ],
  "recommended_checks": [
    "Compare connection pool saturation before and after deployment."
  ]
}


The IDs above are illustrative. At runtime, the backend must resolve evidence IDs to actual stored records and verify access before presenting the response.
AI engineering requirements
- Provider adapters for OpenAI, Anthropic and a mock provider for tests.
- Timeouts, bounded retries, rate limiting and token-budget limits.
- Prompt versioning and model/version metadata on every investigation.
- Explicit handling of empty retrieval results and model refusal.
- Protection against prompt injection in imported documents.
- No secrets, credentials or unnecessary personal information in model prompts.
- Evaluation datasets containing representative incidents, expected source documents and reviewer-approved outcomes.
- Human feedback and regression tests for prompt or model changes.
Use evaluation from the beginning rather than relying on impressive-looking sample responses. The OpenAI evaluation best practices and accuracy optimization guide explain why retrieval quality and generation quality need separate measurement. 

OpenAI API
+1



11. REST API design
Version the API from the beginning using /api/v1/. Generate OpenAPI documentation from the implemented endpoints and validate that the React client uses the same contract.
Method	Endpoint	Purpose
POST	/api/v1/events/ingest	Ingest one or more operational events
GET	/api/v1/incidents	Filter and paginate incidents
GET	/api/v1/incidents/{id}	Retrieve incident details and timeline
POST	/api/v1/incidents/{id}/acknowledge	Acknowledge an incident
POST	/api/v1/incidents/{id}/investigations	Queue an AI investigation
GET	/api/v1/investigations/{id}	Read job status and analysis results
POST	/api/v1/hypotheses/{id}/feedback	Accept, reject or correct a hypothesis
POST	/api/v1/knowledge/documents	Upload a knowledge document
GET	/api/v1/knowledge/search	Search authorized knowledge sources
POST	/api/v1/incidents/{id}/postmortems	Generate a postmortem draft
GET	/api/v1/services	List authorized monitored services
GET	/api/v1/analytics/reliability	Retrieve reliability and incident metrics
Implement pagination, input validation, consistent error responses, permission checks and request IDs. The event-ingestion endpoint should support an idempotency mechanism and enforce payload size limits.
WebSocket contract
Use Django Channels for authenticated, tenant-authorized incident subscriptions.

Example logical event:
{
  "type": "investigation.completed",
  "incident_id": "incident-123",
  "investigation_id": "investigation-456",
  "occurred_at": "2026-10-19T10:30:00Z"
}


The example IDs and timestamp are illustrative. A WebSocket message should normally carry a minimal notification, with the client fetching the authoritative resource over REST. Do not send sensitive incident data to every connected client in a global broadcast.
12. Frontend product design
Build the React application around the investigation workflow rather than a generic administration dashboard.









A. Reliability overview

Active incidents, severity distribution, incident frequency, service health and mean time to acknowledge and recover.












B. Incident workspace

Event timeline, severity, service dependencies, assignment, investigation status and live updates.












C. AI investigation workbench

Ranked hypotheses, cited evidence, missing information, suggested checks and engineer feedback.












D. Service topology

A navigable dependency graph highlighting affected services and related incidents.












E. Postmortem editor

An editable report containing impact, timeline, contributing factors, corrective actions, owners and deadlines.



Use TypeScript types generated from OpenAPI where practical. Include loading, empty, retry and failure states; a real-time interface should also indicate when its WebSocket connection is stale.
13. AI-assisted development workflow
The job description explicitly mentions AI-assisted development. Demonstrate that you can use AI tools to accelerate engineering without allowing them to dictate architecture or introduce unverified code.

Use this workflow throughout the repository.
#chatgpt-mermaid-_r_1an_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-_r_1an_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_1an_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_1an_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-_r_1an_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-_r_1an_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-_r_1an_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-_r_1an_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-_r_1an_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-_r_1an_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-_r_1an_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-_r_1an_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_1an_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_1an_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-_r_1an_ p{margin:0;}#chatgpt-mermaid-_r_1an_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_1an_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_1an_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_1an_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-_r_1an_ .label text,#chatgpt-mermaid-_r_1an_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_1an_ .node rect,#chatgpt-mermaid-_r_1an_ .node circle,#chatgpt-mermaid-_r_1an_ .node ellipse,#chatgpt-mermaid-_r_1an_ .node polygon,#chatgpt-mermaid-_r_1an_ .node path{fill:rgb(17, 40, 19);stroke:rgb(58, 132, 63);stroke-width:1px;}#chatgpt-mermaid-_r_1an_ .rough-node .label text,#chatgpt-mermaid-_r_1an_ .node .label text,#chatgpt-mermaid-_r_1an_ .image-shape .label,#chatgpt-mermaid-_r_1an_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-_r_1an_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-_r_1an_ .rough-node .label,#chatgpt-mermaid-_r_1an_ .node .label,#chatgpt-mermaid-_r_1an_ .image-shape .label,#chatgpt-mermaid-_r_1an_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-_r_1an_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-_r_1an_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_1an_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-_r_1an_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-_r_1an_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-_r_1an_ .edgeLabel{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-_r_1an_ .edgeLabel p{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-_r_1an_ .edgeLabel rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_1an_ .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#chatgpt-mermaid-_r_1an_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-_r_1an_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_1an_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_1an_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-_r_1an_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_1an_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-_r_1an_ .icon-shape,#chatgpt-mermaid-_r_1an_ .image-shape{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-_r_1an_ .icon-shape p,#chatgpt-mermaid-_r_1an_ .image-shape p{background-color:rgb(0, 0, 0);padding:2px;}#chatgpt-mermaid-_r_1an_ .icon-shape .label rect,#chatgpt-mermaid-_r_1an_ .image-shape .label rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_1an_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-_r_1an_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-_r_1an_ .node .neo-node{stroke:rgb(58, 132, 63);}#chatgpt-mermaid-_r_1an_ [data-look="neo"].node rect,#chatgpt-mermaid-_r_1an_ [data-look="neo"].cluster rect,#chatgpt-mermaid-_r_1an_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-_r_1an_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_1an_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-_r_1an_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-_r_1an_-gradient);stroke-width:1px;}#chatgpt-mermaid-_r_1an_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_1an_ [data-look="neo"].node .neo-line path{stroke:rgb(58, 132, 63);filter:none;}#chatgpt-mermaid-_r_1an_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-_r_1an_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_1an_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-_r_1an_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-_r_1an_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_1an_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-_r_1an_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_1an_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(140, 223, 173);}#chatgpt-mermaid-_r_1an_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(140, 223, 173);}#chatgpt-mermaid-_r_1an_ .node tspan[font-weight="normal"],#chatgpt-mermaid-_r_1an_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-_r_1an_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(2, 28, 12);stroke:rgb(26, 75, 45);stroke-width:1px;}#chatgpt-mermaid-_r_1an_ .node rect,#chatgpt-mermaid-_r_1an_ .node circle,#chatgpt-mermaid-_r_1an_ .node ellipse,#chatgpt-mermaid-_r_1an_ .node polygon,#chatgpt-mermaid-_r_1an_ .node path{fill:rgb(0, 55, 22);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-_r_1an_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-_r_1an_ .node.mermaid-decision .label-container{fill:rgb(2, 28, 12);stroke:rgb(26, 75, 45);stroke-dasharray:2,2;}#chatgpt-mermaid-_r_1an_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-_r_1an_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_1an_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}Write issue and acceptancecriteriaAsk AI to analyze the existingcode and propose a planReview architecture, securityand edge casesImplement a small changeRun formatters, type checksand testsInspect diff and dependencychangesRun integration and regressiontestsDocument decisions and opena pull requestHuman review and mergeFailureUnsafe or incorrect





Practical AI tooling
- Use GitHub Copilot, ChatGPT or another coding assistant to explore unfamiliar code, propose test cases, review diffs and draft documentation.
- Use an LLM to generate candidate test data and adversarial RAG examples, then verify those cases independently.
- Use AI to explain failing tests and compare alternative designs, but validate every suggested change through executable tests.
- Keep credentials in environment variables or secret stores; never place them in prompts, committed files or sample logs.
- Require human review for authentication, tenant isolation, database migrations, permission checks and AI-generated remediation logic.
Repository evidence of AI-assisted development
Include docs/ai/engineering-workflow.md documenting:
- Which tasks used AI assistance and what was manually reviewed.
- The test and static-analysis checks run on generated code.
- Representative prompt versions and AI evaluation results.
- A real example of an AI-generated change that failed testing and how you corrected it.
- Decisions where a simpler deterministic algorithm was chosen over an LLM.
The objective is to demonstrate engineering judgment and productivity, not simply to show that a coding assistant was used.
14. Step-by-step implementation roadmap
Build the project in vertical slices. Each phase should leave the repository in a working, testable state.

Phase 1 — Foundation and architecture
Milestone: reproducible development environment
- Create the monorepo and Django/React applications.
- Configure Docker Compose for PostgreSQL with pgvector, Redis, Django and Celery.
- Add environment-specific settings, health checks, formatting and CI.
- Write initial ADRs, requirements and architecture diagrams.




Phase 2 — Domain and secure API
Milestone: an authorized user can report and inspect an incident
- Implement organizations, memberships, roles and services.
- Build event ingestion, idempotency, incident lifecycle and audit history.
- Add Django migrations, indexes, API pagination and OpenAPI.
- Test tenant isolation and invalid state transitions.




Phase 3 — Event processing and live updates
Milestone: an incoming event appears in the incident console
- Implement event normalization, fingerprinting and correlation.
- Add Celery tasks, retry policies and failure handling.
- Integrate Channels and Redis for authenticated live updates.
- Build the incident list, detail page and timeline.




Phase 4 — Knowledge ingestion and RAG
Milestone: engineers can retrieve relevant past incidents and runbooks
- Add document upload, versioning, chunking and embeddings.
- Implement tenant-scoped hybrid retrieval.
- Display retrieved source passages and metadata.
- Benchmark retrieval against a small, labeled test dataset.




Phase 5 — AI investigation
Milestone: an incident receives evidence-linked hypotheses
- Integrate the provider adapter and structured output validation.
- Save investigation jobs, outputs and human feedback.
- Handle provider timeouts, rate limits and missing evidence.
- Add prompt versioning, regression evaluations and failure cases.




Phase 6 — Product workflows and reports
Milestone: a complete investigation-to-postmortem workflow
- Build the service dependency graph.
- Implement hypothesis review, incident assignments and action tracking.
- Generate editable postmortems and reliability analytics.
- Add realistic synthetic incident scenarios and seed data.




Phase 7 — Production readiness
Milestone: repeatable, measurable and documented release
- Run unit, integration, security, UAT and load tests.
- Profile slow queries and tune indexes, pagination and worker concurrency.
- Add tracing, metrics, structured logs and operational alerts.
- Verify backup/restore, migrations, deployment and rollback procedures.



15. Testing and measurable acceptance criteria
A portfolio project is much stronger when you can prove that its features work.
Area	Acceptance criterion
Ingestion	Repeated delivery of the same idempotency key does not create duplicate events
Incident correlation	Known synthetic scenarios produce the expected grouping
Tenant security	Cross-organization requests and retrieval attempts are denied
API	OpenAPI schema validation and API integration tests pass
WebSockets	Authorized clients receive updates; unauthorized clients cannot subscribe
RAG	A versioned benchmark measures retrieval recall and source relevance
AI correctness	Hypotheses are checked against expected outcomes and supporting evidence
Resilience	Provider timeout or queue failure produces a recoverable job state
Frontend	Critical workflows pass browser-based end-to-end tests
Performance	A reproducible load test reports throughput, latency percentiles and error rate
Operations	Logs, metrics and traces allow an engineer to diagnose a deliberately injected failure
Set numerical performance targets only after establishing a baseline on a documented machine and workload. For example, you could adopt an initial target of a p95 response time below 300 ms for ordinary incident-list queries under a defined local load, excluding asynchronous AI processing. Treat this as a test target, not a claim of measured performance.

For AI evaluation, measure at least:
- Retrieval recall at a chosen \(k\), such as recall@5.
- Citation validity and whether sources actually support the associated claim.
- Hypothesis relevance against engineer-reviewed examples.
- Unsupported-claim rate and appropriate abstention when evidence is insufficient.
- Cost and latency per investigation.