import pytest
from pathlib import Path
import json
from datetime import datetime, timedelta, timezone
from logger import CallChemyLogger

@pytest.fixture
def temp_log_dir(tmp_path):
    """Create a temporary directory for test logs"""
    log_dir = tmp_path / "test_logs"
    log_dir.mkdir(exist_ok=True)
    return log_dir

@pytest.fixture
def logger(temp_log_dir):
    """Create a logger instance with test configuration"""
    return CallChemyLogger(
        log_dir=str(temp_log_dir),
        log_file="test.log",
        data_file="test_requests.jsonl",
        retention_days=7
    )

def test_log_success(logger, temp_log_dir):
    """Test successful request logging"""
    conversation_id = "test-123"
    request_data = {"text": "Test request"}
    response_data = {"result": "Test response"}
    
    logger.log_request(conversation_id, request_data, response_data)
    
    data_file = temp_log_dir / "test_requests.jsonl"
    with open(data_file) as f:
        log_entry = json.loads(f.readline())
        assert log_entry["conversation_id"] == conversation_id
        assert log_entry["status"] == "success"
        assert log_entry["request"] == request_data
        assert log_entry["response"] == response_data

def test_log_error(logger, temp_log_dir):
    """Test error logging"""
    conversation_id = "test-456"
    request_data = {"text": "Test request"}
    error = ValueError("Test error")
    
    logger.log_request(conversation_id, request_data, error=error)
    
    data_file = temp_log_dir / "test_requests.jsonl"
    with open(data_file) as f:
        log_entry = json.loads(f.readline())
        assert log_entry["status"] == "error"
        assert log_entry["error"]["type"] == "ValueError"
        assert log_entry["error"]["message"] == "Test error"
        assert "traceback" in log_entry["error"]

def test_cleanup_old_logs(logger, temp_log_dir):
    """Test log retention cleanup"""
    data_file = temp_log_dir / "test_requests.jsonl"
    
    # Create test data with old and new entries
    old_date = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()
    new_date = datetime.now(timezone.utc).isoformat()
    
    with open(data_file, 'w') as f:
        json.dump({"timestamp": old_date, "conversation_id": "old"}, f)
        f.write('\n')
        json.dump({"timestamp": new_date, "conversation_id": "new"}, f)
        f.write('\n')
    
    logger.cleanup_old_logs()
    
    # Verify only new entries remain
    with open(data_file) as f:
        entries = [json.loads(line) for line in f]
        assert len(entries) == 1
        assert entries[0]["conversation_id"] == "new"

def test_empty_log_cleanup(logger, temp_log_dir):
    """Test cleanup with empty log file"""
    data_file = temp_log_dir / "test_requests.jsonl"
    data_file.touch()  # Create empty file
    
    logger.cleanup_old_logs()
    
    assert data_file.exists()
    assert data_file.stat().st_size == 0