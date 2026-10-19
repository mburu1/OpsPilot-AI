from celery import shared_task
from django.utils import timezone

from ai.pipelines.rag_pipeline import RAGPipeline
from ai.providers.openai import OpenAIProvider
from apps.ai_investigations.models import AIInvestigation
from ops_platform.logging.logger import get_logger

logger = get_logger("ai.investigation")


@shared_task(name="ai.investigate_incident")
def investigate_incident_task(investigation_id):
    """Retrieve evidence, analyze an incident, and persist findings."""
    investigation = None
    try:
        investigation = AIInvestigation.objects.get(id=investigation_id)
        investigation.status = "PROCESSING"
        investigation.save(update_fields=["status"])

        logger.info("Starting AI investigation for incident %s", investigation.incident_id)
        provider = OpenAIProvider()
        pipeline = RAGPipeline(provider)
        events = investigation.incident.events.all()
        events_summary = "\n".join(f"[{event.level}] {event.message}" for event in events)
        analysis = pipeline.analyze_incident(
            incident_title=investigation.incident.title,
            events_summary=events_summary,
        )
        investigation.root_cause_hypothesis = analysis["hypothesis"]
        investigation.suggested_remediation = analysis["remediation"]
        investigation.confidence_score = analysis["confidence"]
        investigation.status = "COMPLETED"
        investigation.completed_at = timezone.now()
        investigation.save()
        logger.info("AI investigation completed for incident %s", investigation.incident_id)
    except Exception:
        logger.exception("AI investigation failed for id %s", investigation_id)
        if investigation is not None:
            investigation.status = "FAILED"
            investigation.save(update_fields=["status"])
        raise
