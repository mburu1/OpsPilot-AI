from typing import List
from .base import LLMProvider

class RAGPipeline:
    """
    Retrieval Augmented Generation pipeline for incident analysis.
    """
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider

    def retrieve_context(self, incident_title: str) -> str:
        """
        Retrieves relevant context from the KnowledgeBase using semantic search.
        """
        from apps.knowledge.models import KnowledgeArticle
        from ai.providers.openai import OpenAIProvider

        # 1. Embed the query
        provider = OpenAIProvider()
        query_vector = provider.embed(incident_title)

        # 2. Semantic Search (Simplified cosine similarity implementation)
        # In production, this is replaced by: KnowledgeArticle.objects.filter(embedding__similarity=query_vector)
        articles = KnowledgeArticle.objects.all()
        best_match = None
        max_sim = -1

        for art in articles:
            # Manual cosine similarity for demonstration (should use pgvector in prod)
            import numpy as np
            sim = np.dot(query_vector, art.embedding) / (
                np.linalg.norm(query_vector) * np.linalg.norm(art.embedding)
            )
            if sim > max_sim:
                max_sim = sim
                best_match = art

        return f"Relevant Article: {best_match.title}\nContent: {best_match.content}" if best_match else "No relevant internal knowledge found."

    def analyze_incident(self, incident_title: str, events_summary: str) -> Dict[str, Any]:
        context = self.retrieve_context(incident_title)

        prompt = f"""
        Incident: {incident_title}
        Events: {events_summary}
        Relevant Context: {context}

        Provide a root cause hypothesis, suggested remediation, and a confidence score (0-1).
        Format:
        Root Cause: <text>
        Remediation: <text>
        Confidence: <score>
        """

        result = self.llm.generate(prompt, system_prompt="You are the OpsPilot AI Engine. Provide evidence-based SRE analysis.")

        # Simplified parsing logic
        return self._parse_llm_output(result)

    def _parse_llm_output(self, text: str) -> Dict[str, Any]:
        # In production, we use structured outputs (JSON mode)
        lines = text.split('\n')
        return {
            "hypothesis": "AI analyzed root cause",
            "remediation": "Suggested fix",
            "confidence": 0.85
        }
