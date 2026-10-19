import random
from celery import shared_task
from django.utils import timezone
from ops_platform.observability.slo import SLODefinition, SLOViolation
from ops_platform.logging.logger import get_logger

logger = get_logger("observability.slo")

@shared_task(name="observability.check_slos")
def check_slos_task():
    """Check SLO definitions and record violations."""
    for slo in SLODefinition.objects.filter(is_active=True):
        # Placeholder metric source; replace with Prometheus/Datadog in production.
        current_value = random.uniform(100, 300)
        if current_value > slo.target_value:
            logger.warning("SLO violation for %s: %s > %s", slo.service_name, current_value, slo.target_value)
            SLOViolation.objects.create(
                slo=slo, start_time=timezone.now(), actual_value=current_value,
                organization_id=slo.organization_id,
            )
