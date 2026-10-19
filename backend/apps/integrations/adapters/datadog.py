import requests
from .base import IntegrationAdapter

class DatadogAdapter(IntegrationAdapter):
    """
    Integration for Datadog events/metrics.
    """
    def __init__(self, api_key, app_key):
        self.api_key = api_key
        self.app_key = app_key
        self.base_url = "https://api.datadoghq.com/api/v1/events"

    def fetch_events(self):
        params = {"filter": "source:opspilot"}
        response = requests.get(self.base_url, params=params, auth=(self.app_key, self.api_key))
        return response.json().get('events', [])

    def parse_event(self, raw_data):
        return {
            "message": raw_data.get('msg'),
            "level": raw_data.get('alert_type', 'INFO'),
            "metadata": raw_data
        }
