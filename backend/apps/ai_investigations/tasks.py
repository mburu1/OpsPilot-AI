from celery import shared_task
from django.utils import timezone
from apps.ai_investigations.models import AIInvestigation
from ai.providers.openai import OpenAIProvider
from ai.pipelines.rag_pipeline import RAGPipeline
from platform.logging.logger import get_logger

logger = get_logger('ai.investigation')

@shared_task(name='ai.investigate_incident')
def investigate_incident_task(investigation_id):
    """
    The core AI pipeline task:
    1. Retrieve evidence
    2. Call LLM via RAG
    3. Store results in the database
    """
    try:
        investigation = AIInvestigation.objects.get(id=investigation_id)
        investigation.status = 'PROCESSING'
        investigation.save()

        logger.info(f"Starting AI investigation for incident {investigation.incident.id}")

        # Setup AI pipeline
        provider = OpenAIProvider()
        pipeline = RAGPipeline(provider)

        # Gather evidence from associated events
        events = investigation.incident.events.all()
        events_summary = "\n".join([f"[{e.level}] {e.message}" for e in events])

        # Run RAG analysis
        analysis = pipeline.analyze_incident(
            incident_title=investigation.incident.title,
            events_summary=events_summary
        )

        # Store findings
        investigation.root_cause_hypothesis = analysis['hypothesis']
        investigation.suggested_remediation = analysis['remediation']
        investigation.confidence_score = analysis['confidence']
        investigation.status = 'COMPLETED'
        investigation.completed_at = timezone.now()
        investigation.save()

        logger.info(f"AI investigation completed for {investigation.incident.id}")

    except Exception as e:
        logger.error(f"AI investigation failed: {str(e)}")
        # Update status to FAILED if possible
        try:
            investigation.status = 'FAILED'
            investigation.save()
        except:
            pass
