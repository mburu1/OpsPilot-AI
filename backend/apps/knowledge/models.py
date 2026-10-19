from django.db import models
from platform.authentication.models import BaseTenantModel

class KnowledgeArticle(BaseTenantModel):
    """
    Engineering documentation, runbooks, and post-mortem archives.
    """
    title = models.CharField(max_length=500)
    content = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)

    # Path to the original source (e.g., Confluence link, GitHub MD file)
    source_url = models.URLField(blank=True, null=True)

    # Vector embedding stored as a list of floats (or using pgvector's VectorField)
    # Using JSONField here for generic compatibility, but pgvector is recommended for prod.
    embedding = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
