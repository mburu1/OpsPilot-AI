from celery import shared_task
from django.utils import timezone
from platform.observability.slo import SLODefinition, SLOViolation
from platform.logging.logger import get_logger
import random # Simulated metric fetcher

logger = get_logger('observability.slo')

@shared_task(name='observability.check_slos')
def check_slos_task():
    """
    Background task that monitors metrics against SLO definitions.
    Triggers incidents if SLOs are violated.
    """
    slos = SLODefinition.objects.filter(is_active=True)

    for slo in slos:
        # In production, this would call Prometheus/Datadog API
        # current_value = prometheus.query(slo.metric_name)
        current_value = random.uniform(100, 300)

        if current_value > slo.target_value:
            logger.warning(f"SLO Violation detected for {slo.service_name}: {current_value} > {slo.target_value}")

            # Create an SLO Violation record
            violation = SLOViolation.objects.create(
                slo=slo,
                start_time=timezone.now(),
                actual_value=current_value
            )

            # Trigger the Correlation Engine to create an Incident
            from apps.correlations.tasks import process_events_task
            process_events_task.delay()
