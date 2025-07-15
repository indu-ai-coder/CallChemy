"""Tests for the summarization module."""
import pytest
from ..summarizer.models import SummaryRequest, Summary, SummaryStyle

@pytest.fixture
def sample_conversation():
    return {
        "conversation_id": "test-123",
        "utterances": [
            {"speaker": "Customer", "text": "Hi, I'm having trouble with my credit card payment."},
            {"speaker": "Agent", "text": "I understand you're having issues with your credit card payment. I'll help you resolve this."},
            {"speaker": "Customer", "text": "Thank you, that would be great!"}
        ]
    }

@pytest.fixture
def summary_request(sample_conversation):
    return SummaryRequest(
        conversation_id=sample_conversation["conversation_id"],
        utterances=sample_conversation["utterances"],
        style=SummaryStyle.BRIEF
    )

def test_summary_request_validation(summary_request):
    """Test that a valid summary request passes validation."""
    assert summary_request.conversation_id == "test-123"
    assert len(summary_request.utterances) == 3
    assert summary_request.style == SummaryStyle.BRIEF

def test_summary_response_validation():
    """Test that a valid summary response passes validation."""
    summary = Summary(
        conversation_id="test-123",
        summary="Customer reported credit card payment issues. Agent offered to help resolve the problem.",
        key_points=["Payment issue reported", "Agent offered assistance"],
        action_items=["Resolve credit card payment problem"],
        next_steps=["Verify payment status", "Process payment"],
        confidence_score=0.95
    )
    
    assert summary.conversation_id == "test-123"
    assert len(summary.key_points) == 2
    assert 0 <= summary.confidence_score <= 1

@pytest.mark.parametrize("style", [
    SummaryStyle.BRIEF,
    SummaryStyle.DETAILED,
    SummaryStyle.ACTION_ITEMS
])
def test_summary_styles(style, summary_request):
    """Test that all summary styles are supported."""
    summary_request.style = style
    assert summary_request.style == style
