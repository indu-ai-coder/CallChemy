"""Fallback provider using local models for offline support."""
from typing import Optional
from transformers import pipeline
from .base import LLMProvider, LLMError

class FallbackLLMProvider(LLMProvider):
    """Local model fallback for summarization."""
    
    def __init__(self):
        """Initialize local summarization model."""
        try:
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1  # CPU
            )
        except Exception as e:
            raise LLMError(f"Failed to initialize fallback model: {str(e)}")
    
    async def generate_summary(
        self,
        context: str,
        prompt: str,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate summary using local model.
        
        Args:
            context: Conversation text
            prompt: Instruction prompt (used for length guidance)
            max_tokens: Optional max length
            
        Returns:
            str: Generated summary
        """
        self._validate_inputs(context, prompt)
        
        try:
            # Convert max_tokens to max_length (roughly)
            max_length = max_tokens // 4 if max_tokens else 130
            min_length = max(30, max_length // 2)
            
            result = self.summarizer(
                context,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )[0]["summary_text"]
            
            return self._format_response(result)
            
        except Exception as e:
            raise LLMError(f"Fallback model error: {str(e)}")
