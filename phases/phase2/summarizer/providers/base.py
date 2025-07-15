"""Base protocol for LLM providers."""
from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass

@dataclass
class LLMResponse:
    """Structured response from LLM provider."""
    text: str
    confidence: float
    provider: str

class LLMError(Exception):
    """Base exception for LLM-related errors."""
    pass

class LLMProvider(ABC):
    """Abstract base class defining the interface for LLM providers."""
    
    @abstractmethod
    async def generate_summary(
        self,
        context: str,
        prompt: str,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a summary using the LLM provider.
        
        Args:
            context: The conversation text to summarize
            prompt: The instruction prompt for the LLM
            max_tokens: Optional maximum length for the response
            
        Returns:
            str: The generated summary
            
        Raises:
            LLMError: If there's an error in generation
            ValueError: If inputs are invalid
        """
        pass
    
    def _validate_inputs(self, context: str, prompt: str) -> None:
        """Validate input parameters."""
        if not context or not context.strip():
            raise ValueError("Context cannot be empty")
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
    
    def _format_response(self, text: str) -> str:
        """Format the response text."""
        return text.strip()
