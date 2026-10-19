# Class Diagram

Detailed implementation structure for the AI Investigation module.

```mermaid
classDiagram
    class AIInvestigationManager {
        +startInvestigation(incidentId)
        +getAnalysis(investigationId)
    }
    class RAGPipeline {
        +retrieveContext(query)
        +augmentPrompt(context)
        +generateResponse()
    }
    class VectorStore {
        +query(vector)
        +upsert(doc)
    }
    class LLMClient {
        +call(prompt)
        +stream(prompt)
    }
    class AnalysisResult {
        +String rootCause
        +List recommendations
        +float confidenceScore
    }

    AIInvestigationManager --> RAGPipeline : uses
    RAGPipeline --> VectorStore : retrieves from
    RAGPipeline --> LLMClient : invokes
    AIInvestigationManager ..> AnalysisResult : produces
