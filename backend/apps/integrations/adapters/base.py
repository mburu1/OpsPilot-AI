from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IntegrationAdapter(ABC):
    """
    Abstract base class for external data ingestion.
    """
    @abstractmethod
    def fetch_events(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def parse_event(self, raw_data: Any) -> Dict[str, Any]:
        pass
