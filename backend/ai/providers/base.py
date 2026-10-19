from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LLMProvider(ABC):
    """
    Abstract base class for LLM providers (e.g., OpenAI, Claude).
    """
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        pass

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        pass
