from abc import ABC, abstractmethod
from typing import Dict, Any

class NotificationProvider(ABC):
    """
    Abstract base for notification channels (Slack, Teams, Email).
    """
    @abstractmethod
    def send(self, channel_id: str, message: str, payload: Dict[str, Any] = None):
        pass
