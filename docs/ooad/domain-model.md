# Domain Model

The OpsPilot AI domain focuses on the lifecycle of an operational incident from detection to resolution.

```mermaid
classDiagram
    class Organization {
        +String name
        +String domain
        +getMembers()
    }
    class Account {
        +String email
        +Role role
        +authenticate()
    }
    class Service {
        +String name
        +String version
        +ServiceStatus status
    }
    class Event {
        +DateTime timestamp
        +LogLevel level
        +String message
        +JSON metadata
    }
    class Incident {
        +String incidentId
        +IncidentPriority priority
        +IncidentStatus status
        +associateEvents(Events[])
    }
    class Investigation {
        +String investigationId
        +String aiSummary
        +InvestigationStatus status
        +generateRootCause()
    }
    class KnowledgeBase {
        +String articleId
        +String content
        +search(query)
    }

    Organization "1" -- "*" Account : manages
    Organization "1" -- "*" Service : owns
    Service "1" -- "*" Event : generates
    Event "*" -- "0..1" Incident : triggers
    Incident "1" -- "1" Investigation : leads_to
    Investigation "*" -- "*" KnowledgeBase : references
