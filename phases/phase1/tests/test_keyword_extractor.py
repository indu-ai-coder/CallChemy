import pytest
from keyword_extractor import KeywordExtractor

@pytest.fixture
def extractor():
    return KeywordExtractor()

def test_financial_terms(extractor):
    """Test extraction of financial terms"""
    text = "My payment of ₹5000 was declined for account #12345"
    result = extractor.extract_keywords(text)
    
    assert "₹5000" in result['financial_terms']
    assert "account #12345" in result['financial_terms']

def test_product_detection(extractor):
    """Test product term detection"""
    text = "I need help with my credit card and savings account"
    result = extractor.extract_keywords(text)
    
    assert "credit card" in result['products']
    assert "savings" in result['products']

def test_action_detection(extractor):
    """Test action term detection"""
    text = "My transaction was declined and is now pending"
    result = extractor.extract_keywords(text)
    
    assert "declined" in result['actions']
    assert "pending" in result['actions']

def test_transcript_analysis(extractor):
    """Test full transcript analysis"""
    utterances = [
        {
            "speaker": "Customer",
            "text": "My credit card payment of ₹10,000 was declined"
        },
        {
            "speaker": "Agent",
            "text": "I'll check why the payment failed"
        }
    ]
    results = extractor.analyze_transcript(utterances)
    
    assert "₹10,000" in results[0]['keywords']['financial_terms']
    assert "credit card" in results[0]['keywords']['products']
    assert "declined" in results[0]['keywords']['actions']
    assert "failed" in results[1]['keywords']['actions']