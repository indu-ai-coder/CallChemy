import pytest
from fastapi.testclient import TestClient
from phases.phase1.api.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "CallChemy API" in response.json()["title"]

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"

def test_analyze_endpoint_without_api_key():
    response = client.post("/analyze")
    assert response.status_code == 422  # Missing API key

def test_analyze_endpoint_with_invalid_api_key():
    response = client.post("/analyze?api_key=invalid-key")
    assert response.status_code == 401

def test_analyze_endpoint_success():
    test_data = {
        "conversation_id": "test-001",
        "transcript": [
            {
                "speaker": "Customer",
                "text": "Hi, I am having trouble with my credit card payment."
            },
            {
                "speaker": "Agent",
                "text": "I understand you're having issues with your credit card payment. I'll help you resolve this."
            }
        ]
    }
    
    response = client.post(
        "/analyze?api_key=callchemy-test-key",
        json=test_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"] == "test-001"
    assert "timestamp" in data
    assert "analysis" in data
    assert len(data["analysis"]["utterances"]) == 2

def test_analyze_endpoint_invalid_input():
    test_data = {
        "conversation_id": "test-001",
        "transcript": [
            {
                "speaker": "Invalid",  # Invalid speaker role
                "text": "Hi there"
            }
        ]
    }
    
    response = client.post(
        "/analyze?api_key=callchemy-test-key",
        json=test_data
    )
    assert response.status_code == 422

def test_analyze_endpoint_empty_transcript():
    test_data = {
        "conversation_id": "test-001",
        "transcript": []
    }
    
    response = client.post(
        "/analyze?api_key=callchemy-test-key",
        json=test_data
    )
    assert response.status_code == 422

@pytest.mark.performance
def test_analyze_endpoint_performance():
    test_data = {
        "conversation_id": "perf-001",
        "transcript": [{"speaker": "Customer", "text": "Hello"}] * 10
    }
    
    start_time = pytest.importorskip("time").time()
    response = client.post(
        "/analyze?api_key=callchemy-test-key",
        json=test_data
    )
    end_time = pytest.importorskip("time").time()
    
    assert response.status_code == 200
    assert (end_time - start_time) < 2.0  # Should process in under 2 seconds

def test_cors_headers():
    response = client.options("/")
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"

def test_error_response_format():
    response = client.post("/analyze")  # Missing API key will trigger error
    assert response.status_code == 422
    error_response = response.json()
    assert "detail" in error_response
