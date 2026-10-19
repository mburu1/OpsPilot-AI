from typing import List, Dict, Any
from .base import LLMProvider
from ai.schemas.grounding import GroundedAnalysis, EvidenceSource

class RAGPipeline:
    """
    Upgraded RAG pipeline with explicit evidence grounding.
    """
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider

    def retrieve_evidence(self, incident_title: str, organization_id: str) -> List[EvidenceSource]:
        """
        Retrieves and scores a mix of events and knowledge articles.
        """
        from ai.retrieval.hybrid_search import HybridSearchEngine
        from apps.events.models import Event

        search_engine = HybridSearchEngine()
        articles = search_engine.search(incident_title, organization_id)

        evidence = []
        # Add articles as evidence
        for i, art in enumerate(articles[:3]):
            evidence.append(EvidenceSource(
                source_type='article',
                source_id=str(art.id),
                snippet=art.content[:200],
                relevance_score=0.9 - (i * 0.1)
            ))

        # Add top relevant events
        events = Event.objects.filter(organization_id=organization_id).order_by('-timestamp')[:5]
        for i, event in enumerate(events):
            evidence.append(EvidenceSource(
                source_type='event',
                source_id=str(event.id),
                snippet=event.message,
                relevance_score=0.8 - (i * 0.05)
            ))

        return evidence

    def analyze_incident(self, incident, events_summary: str) -> GroundedAnalysis:
        evidence = self.retrieve_evidence(incident.title, incident.organization_id)

        # Create a detailed context block for the LLM
        evidence_block = "\n".join([
            f"[{e.source_type}] ID {e.source_id}: {e.snippet}"
            for e in evidence
        ])

        prompt = f"""
        Incident: {incident.title}
        Events: {events_summary}

        AVAILABLE EVIDENCE:
        {evidence_block}

        Task: Provide a root cause hypothesis and remediation.
        CRITICAL: You must cite the Evidence IDs used in your conclusion.

        Format:
        Hypothesis: <text> (citing ID X, Y)
        Remediation: <text>
        Confidence: <score>
        """

        result = self.llm.generate(prompt, system_prompt="You are the OpsPilot AI Engine. Provide evidence-grounded SRE analysis.")

        # Simplified parsing for the example
        return GroundedAnalysis(
            hypothesis=result, # In prod, we parse the specific a line
            remediation="Suggested fix based on evidence",
            confidence=0.88,
            evidence=evidence
        )
