from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from apps.events.models import Event
from apps.incidents.models import Incident
from apps.correlations.models import CorrelationRule
from platform.logging.logger import get_logger

logger = get_logger('correlations.engine')

@shared_task(name='correlations.process_events')
def process_events_task():
    """
    Background task that scans recent events and creates incidents
    based on active CorrelationRules.
    """
    logger.info("Starting event correlation scan...")

    # Scan window: look at events from the last 15 minutes
    window_start = timezone.now() - timedelta(minutes=15)

    # Get all active rules
    rules = CorrelationRule.objects.filter(is_active=True)

    for rule in rules:
        # Simplified Correlation Logic:
        # We assume rule.logic_config contains {'threshold': X, 'time_window_minutes': Y}
        config = rule.logic_config
        threshold = config.get('threshold', 5)
        window_mins = config.get('time_window_minutes', 5)

        # Find events that match the rule's criteria
        # In a real production system, this would use a more complex query or a stream processor
        events = Event.objects.filter(
            timestamp__gte=timezone.now() - timedelta(minutes=window_mins),
            # We'd filter by service or level here based on the rule config
        )

        # Group by organization to ensure tenant isolation
        org_ids = events.values_list('organization_id', flat=True).distinct()

        for org_id in org_ids:
            org_events = events.filter(organization_id=org_id)
            if org_events.count() >= threshold:
                # Create an incident if one doesn't already exist for this pattern
                Incident.objects.get_or_create(
                    defaults={
                        'title': f"Automated Incident: {rule.name}",
                        'description': f"Triggered by rule {rule.name} with {org_events.count()} events.",
                        'organization_id': org_id,
                        'priority': rule.priority_override or 'MEDIUM',
                        'status': 'OPEN'
                    }
                )
                # Associate the events
                incident, _ = Incident.objects.filter(title__contains=rule.name, organization_id=org_id).latest('created_at')
                incident.events.add(*org_events)

    logger.info("Event correlation scan completed.")
