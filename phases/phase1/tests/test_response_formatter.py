import pytest
from phases.phase1.response_formatter import ResponseFormatter
from datetime import datetime

@pytest.fixture
def formatter():
    return ResponseFormatter()

def test_full_response(formatter):
    """Test formatting with all modules' output"""
    conversation_id = "test-123"
    utterances = [
        {
            "speaker": "Customer",
            "text": "My card is blocked",
            "intent": "card_problem",
            "sentiment": "negative",
            "keywords": {
                "products": ["card"],
                "actions": ["blocked"]
            }
        },
        {
            "speaker": "Agent",
            "text": "I'll help you unblock it",
            "intent": "no_intent_detected",
            "sentiment": "not_analyzed",
            "keywords": {
                "actions": ["unblock"]
            }
        }
    ]
    summary = {
        "paragraph": "Customer reported blocked card issue.",
        "bullet_points": ["Card blocked", "Agent offered help"]
    }

    result = formatter.format_response(conversation_id, utterances, summary)

    assert result["conversation_id"] == conversation_id
    assert isinstance(result["timestamp"], str)
    assert result["overall_sentiment"] == "negative"
    assert result["primary_intent"] == "card_problem"
    assert "card" in str(result["utterances"][0]["keywords"]["products"])

def test_missing_fields(formatter):
    """Test handling of missing optional fields"""
    conversation_id = "test-456"
    utterances = [
        {
            "speaker": "Customer",
            "text": "Hello"
        }
    ]

    result = formatter.format_response(conversation_id, utterances)

    assert result["conversation_id"] == conversation_id
    assert result["utterances"][0]["intent"] == "no_intent_detected"
    assert result["utterances"][0]["sentiment"] == "not_analyzed"
    assert result["summary"] is None