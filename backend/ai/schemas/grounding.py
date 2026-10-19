from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class EvidenceSource:
    source_type: str # 'event', 'article', 'metric'
    source_id: str
    snippet: str
    relevance_score: float

class GroundedAnalysis:
    """
    Wraps AI analysis with explicit evidence citations.
    """
    def __init__(self, hypothesis: str, remediation: str, confidence: float, evidence: List[EvidenceSource]):
        self.hypothesis = hypothesis
        self.remediation = remediation
        self.confidence = confidence
        self.evidence = evidence

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hypothesis": self.hypothesis,
            "remediation": self.remediation,
            "confidence": self.confidence,
            "evidence": [
                {"type": e.source_type, "id": e.source_id, "text": e.snippet, "score": e.relevance_score}
                for e in self.evidence
            ]
        }
