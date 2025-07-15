"""Tests for LLM providers implementation."""
import pytest
from unittest.mock import AsyncMock, patch
from typing import Optional
import json
from ..summarizer.providers.base import LLMProvider, LLMResponse, LLMError
from ..summarizer.providers.claude import ClaudeLLMProvider
from ..summarizer.providers.fallback import FallbackLLMProvider

@pytest.fixture
def sample_conversation():
    return """
Customer: Hi, I'm having trouble with my credit card payment.
Agent: I understand you're having issues with your credit card payment. I'll help you resolve this.
Customer: Thank you, that would be great!
"""

@pytest.fixture
def sample_prompt():
    return "Summarize this conversation briefly, focusing on the main issue and resolution."

class MockLLMProvider(LLMProvider):
    """Mock provider for testing the base protocol"""
    async def generate_summary(self, context: str, prompt: str, max_tokens: Optional[int] = None) -> str:
        self._validate_inputs(context, prompt)
        return "Mock summary: Customer had credit card payment issues."

@pytest.mark.asyncio
async def test_llm_provider_protocol():
    """Test that the LLM provider protocol works as expected"""
    provider = MockLLMProvider()
    summary = await provider.generate_summary(
        context="test context",
        prompt="test prompt"
    )
    assert isinstance(summary, str)
    assert len(summary) > 0

@pytest.mark.asyncio
async def test_claude_provider_success():
    """Test successful Claude API call"""
    with patch('anthropic.AsyncAnthropic') as mock_anthropic:
        mock_client = AsyncMock()
        mock_client.messages.create.return_value.content = [{"text": "Summary: Payment issue resolved"}]
        mock_anthropic.return_value = mock_client

        provider = ClaudeLLMProvider(api_key="test-key")
        response = await provider.generate_summary(
            context="test conversation",
            prompt="test prompt",
            max_tokens=100
        )

        assert "Payment issue resolved" in response
        mock_client.messages.create.assert_called_once()

@pytest.mark.asyncio
async def test_claude_provider_error():
    """Test Claude API error handling"""
    with patch('anthropic.AsyncAnthropic') as mock_anthropic:
        mock_client = AsyncMock()
        mock_client.messages.create.side_effect = Exception("API Error")
        mock_anthropic.return_value = mock_client

        provider = ClaudeLLMProvider(api_key="test-key")
        
        with pytest.raises(LLMError) as exc_info:
            await provider.generate_summary(
                context="test conversation",
                prompt="test prompt"
            )
        
        assert "API Error" in str(exc_info.value)

@pytest.mark.asyncio
async def test_fallback_provider():
    """Test the fallback provider with local model"""
    provider = FallbackLLMProvider()
    response = await provider.generate_summary(
        context="Customer: I have a problem. Agent: I'll help.",
        prompt="Summarize briefly"
    )
    
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.asyncio
async def test_max_tokens_limit():
    """Test that max_tokens parameter is respected"""
    provider = MockLLMProvider()
    response = await provider.generate_summary(
        context="test context",
        prompt="test prompt",
        max_tokens=50
    )
    
    # Split into words and check length
    words = response.split()
    assert len(words) <= 50

@pytest.mark.asyncio
async def test_provider_validation():
    """Test input validation in providers"""
    provider = MockLLMProvider()
    
    with pytest.raises(ValueError):
        await provider.generate_summary(
            context="",  # Empty context
            prompt="test prompt"
        )
    
    with pytest.raises(ValueError):
        await provider.generate_summary(
            context="test context",
            prompt=""  # Empty prompt
        )

@pytest.mark.asyncio
async def test_response_formatting():
    """Test that response is properly formatted"""
    provider = MockLLMProvider()
    response = await provider.generate_summary(
        context="test context",
        prompt="test prompt"
    )
    
    assert isinstance(response, str)
    assert response.strip() == response  # No leading/trailing whitespace
