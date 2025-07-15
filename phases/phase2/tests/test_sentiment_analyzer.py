import pytest
from phases.phase1.sentiment_analyzer import SentimentAnalyzer

@pytest.fixture
def analyzer():
    return SentimentAnalyzer()

def test_negative_complaint(analyzer):
    """Test detection of negative sentiment in complaints"""
    utterance = {
        "speaker": "Customer",
        "text": "This is terrible service! I'm very frustrated with this issue."
    }
    result = analyzer.analyze_transcript([utterance])[0]
    assert result["sentiment"] == "negative"

def test_neutral_query(analyzer):
    """Test neutral sentiment detection"""
    utterance = {
        "speaker": "Customer",
        "text": "I would like to check my account balance."
    }
    result = analyzer.analyze_transcript([utterance])[0]
    assert result["sentiment"] == "neutral"

def test_positive_statement(analyzer):
    """Test positive sentiment detection"""
    utterance = {
        "speaker": "Customer",
        "text": "Thank you so much for your excellent help today!"
    }
    result = analyzer.analyze_transcript([utterance])[0]
    assert result["sentiment"] == "positive"

def test_agent_utterance(analyzer):
    """Test that agent utterances are not analyzed"""
    utterance = {
        "speaker": "Agent",
        "text": "I'm happy to help you today!"
    }
    result = analyzer.analyze_transcript([utterance])[0]
    assert result["sentiment"] == "not_analyzed"