import pytest
from ingestion import InputValidator

def test_valid_input():
    validator = InputValidator()
    data = {
        "conversation_id": "test-123",
        "transcript": [
            {"speaker": "Customer", "text": "Hello"},
            {"speaker": "Agent", "text": "Hi there"}
        ]
    }
    validated = validator.validate(data)
    assert validated["conversation_id"] == "test-123"
    assert len(validated["transcript"]) == 2

def test_invalid_speaker():
    validator = InputValidator()
    data = {
        "conversation_id": "test-123",
        "transcript": [
            {"speaker": "Invalid", "text": "Hello"}
        ]
    }
    with pytest.raises(ValueError):
        validator.validate(data)

def test_empty_text():
    validator = InputValidator()
    data = {
        "conversation_id": "test-123",
        "transcript": [
            {"speaker": "Customer", "text": ""}
        ]
    }
    with pytest.raises(ValueError):
        validator.validate(data)