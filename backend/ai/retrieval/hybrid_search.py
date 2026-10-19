from django.db.models import Q
from apps.knowledge.models import KnowledgeArticle
from ai.providers.openai import OpenAIProvider
import numpy as np

class HybridSearchEngine:
    """
    Combines Keyword (BM25-style) and Semantic (Vector) search.
    """
    def __init__(self):
        self.provider = OpenAIProvider()

    def search(self, query: str, organization_id: str, top_k: int = 5):
        # 1. Semantic Search (Vector)
        query_vector = self.provider.embed(query)

        # In production, we'd use pgvector's <=> operator
        # Here we simulate the retrieval of candidates
        candidates = KnowledgeArticle.objects.filter(organization_id=organization_id)

        results = []
        for art in candidates:
            # Vector Similarity
            vec_sim = np.dot(query_vector, art.embedding) / (
                np.linalg.norm(query_vector) * np.linalg.norm(art.embedding)
            )

            # Keyword Similarity (Simple overlap for demonstration)
            kw_sim = 0.0
            if query.lower() in art.title.lower() or query.lower() in art.content.lower():
                kw_sim = 1.0

            # Hybrid Score: Weighted average (0.7 semantic, 0.3 keyword)
            final_score = (0.7 * vec_sim) + (0.3 * kw_sim)
            results.append((art, final_score))

        # Sort by score and return top K
        results.sort(key=lambda x: x[1], reverse=True)
        return [res[0] for res in results[:top_k]]
