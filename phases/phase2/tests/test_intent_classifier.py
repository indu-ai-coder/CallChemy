import pytest
from phases.phase1.intent_classifier import IntentClassifier

@pytest.fixture
def classifier():
    return IntentClassifier()

def test_basic_classification(classifier):
    """Test basic intent classification"""
    utterances = [
        {"speaker": "Customer", "text": "I need to check my account balance"},
        {"speaker": "Agent", "text": "I'll help you with that"},
    ]
    results = classifier.analyze_transcript(utterances)
    assert results[0]["intent"] == "account_inquiry"
    assert results[1]["intent"] == "no_intent_detected"

def test_edge_cases(classifier):
    """Test edge cases like greetings and thanks"""
    greetings = [
        {"speaker": "Customer", "text": "Hello"},
        {"speaker": "Customer", "text": "Thank you"},
        {"speaker": "Customer", "text": "Hi there"},
    ]
    results = classifier.analyze_transcript(greetings)
    assert all(r["intent"] == "no_intent_detected" for r in results)

def test_multiple_intents(classifier):
    """Test utterance that could match multiple intents"""
    utterance = {
        "speaker": "Customer",
        "text": "I have a problem with my card transaction"
    }
    result = classifier.analyze_transcript([utterance])[0]
    assert result["intent"] in ["card_problem", "transaction_issue", "complaint"]