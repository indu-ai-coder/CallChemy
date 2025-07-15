"""Claude API integration for summarization."""
import os
from typing import Optional
import anthropic
from .base import LLMProvider, LLMError

class ClaudeLLMProvider(LLMProvider):
    """Implementation of LLMProvider using Anthropic's Claude API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Claude client."""
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            raise ValueError("Claude API key is required")
        
        self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
        self.model = "claude-3-opus-20240229"  # Latest model as of 2025
    
    async def generate_summary(
        self,
        context: str,
        prompt: str,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate summary using Claude API.
        
        Args:
            context: Conversation text
            prompt: Instruction prompt
            max_tokens: Optional max length
            
        Returns:
            str: Generated summary
            
        Raises:
            LLMError: If API call fails
        """
        self._validate_inputs(context, prompt)
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{
                    "role": "user",
                    "content": f"{prompt}\n\nConversation:\n{context}"
                }]
            )
            
            return self._format_response(response.content[0]["text"])
            
        except Exception as e:
            raise LLMError(f"Claude API error: {str(e)}")
