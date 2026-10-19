from celery import shared_task
from ai.providers.openai import OpenAIProvider
from apps.knowledge.models import KnowledgeArticle
from platform.logging.logger import get_logger

logger = get_logger('knowledge.sync')

@shared_task(name='knowledge.vectorize_article')
def vectorize_article_task(article_id):
    """
    Converts a knowledge article's text into a vector embedding
    and stores it for RAG retrieval.
    """
    try:
        article = KnowledgeArticle.objects.get(id=article_id)
        provider = OpenAIProvider()

        # Create embedding of the title and content
        text_to_embed = f"{article.title}\n{article.content}"
        embedding = provider.embed(text_to_embed)

        article.embedding = embedding
        article.save()

        logger.info(f"Vectorized article {article_id} successfully.")
    except Exception as e:
        logger.error(f"Failed to vectorize article {article_id}: {str(e)}")
