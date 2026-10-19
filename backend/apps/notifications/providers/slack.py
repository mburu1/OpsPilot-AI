import requests
from .base import NotificationProvider

class SlackProvider(NotificationProvider):
    """
    Slack integration using Incoming Webhooks.
    """
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, channel_id: str, message: str, payload: Dict[str, Any] = None):
        data = {
            "text": message,
            "attachments": [{"text": str(payload)} if payload else []]
        }
        response = requests.post(self.webhook_url, json=data)
        return response.status_code == 200
