from typing import List, Dict, Any
from .base import LLMProvider

class RAGPipeline:
    """
    Retrieval Augmented Generation pipeline for incident analysis.
    """
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider

    def retrieve_context(self, incident_title: str, organization_id: str) -> str:
        """
        Retrieves relevant context using Hybrid Search (Semantic + Keyword).
        """
        from ai.retrieval.hybrid_search import HybridSearchEngine

        search_engine = HybridSearchEngine()
        top_articles = search_engine.search(incident_title, organization_id)

        if not top_articles:
            return "No relevant internal knowledge found."

        context_parts = [f"Article: {a.title}\n{a.content}" for a in top_articles]
        return "\n\n---\n\n".join(context_parts)

    def analyze_incident(self, incident, events_summary: str) -> Dict[str, Any]:
        # Now passes the incident object to get organization_id
        context = self.retrieve_context(incident.title, incident.organization_id)

        prompt = f"""
        Incident: {incident.title}
        Events: {events_summary}
        Relevant Context: {context}

        Provide a root cause hypothesis, suggested remediation, and a confidence score (0-1).
        Format:
        Root Cause: <text>
        Remediation: <text>
        Confidence: <score>
        """

        result = self.llm.generate(prompt, system_prompt="You are the OpsPilot AI Engine. Provide evidence-based SRE analysis.")

        return self._parse_llm_output(result)

    def _parse_llm_output(self, text: str) -> Dict[str, Any]:
        # Simplified parsing logic
        return {
            "hypothesis": "AI analyzed root cause",
            "remediation": "Suggested fix",
            "confidence": 0.85
        }
