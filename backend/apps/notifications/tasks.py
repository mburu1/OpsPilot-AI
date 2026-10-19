from celery import shared_task
from django.conf import settings
from apps.notifications.models import NotificationChannel
from apps.notifications.providers.slack import SlackProvider
from platform.logging.logger import get_logger

logger = get_logger('notifications.engine')

@shared_task(name='notifications.dispatch_alert')
def dispatch_alert_task(message, payload=None):
    """
    Dispatches an alert to all active notification channels.
    """
    channels = NotificationChannel.objects.filter(is_active=True)

    for channel in channels:
        try:
            if channel.provider_type == 'slack':
                provider = SlackProvider(channel.config.get('webhook_url'))
                provider.send(channel.name, message, payload)
                logger.info(f"Alert sent to Slack channel {channel.name}")
            # Add Teams logic here...
        except Exception as e:
            logger.error(f"Failed to send notification to {channel.name}: {str(e)}")
