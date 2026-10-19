from abc import ABC, abstractmethod
from typing import List, Dict, Any

class StreamProcessor(ABC):
    """
    Abstract base for real-time event streaming (Kafka/RabbitMQ).
    """
    @abstractmethod
    def consume(self, topic: str, callback):
        """
        Start consuming from a topic and trigger a callback for each message.
        """
        pass

    @abstractmethod
    def produce(self, topic: str, message: Dict[str, Any]):
        """
        Publish a message to a specific topic.
        """
        pass
