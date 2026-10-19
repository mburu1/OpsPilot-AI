import os
from openai import OpenAI
from .base import LLMProvider

class OpenAIProvider(LLMProvider):
    """
    Implementation of LLMProvider using OpenAI's API.
    """
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    def generate(self, prompt: str, system_prompt: str = "You are an expert SRE.") -> str:
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2
        )
        return response.choices[0].message.content

    def embed(self, text: str):
        # Simplified embedding call
        response = self.client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
