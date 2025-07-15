# CallChemy

CallChemy is a powerful conversation analysis API that processes customer service interactions to extract meaningful insights. It provides intent classification, sentiment analysis, keyword extraction, and conversation summarization through a FastAPI-based REST API.

## Features

- 🎯 **Intent Classification**: Identifies the purpose and goals in customer conversations
- 😊 **Sentiment Analysis**: Analyzes emotional tone and customer satisfaction
- 🔑 **Keyword Extraction**: Extracts important topics, products, and action items
- 📊 **Conversation Summarization**: Provides structured insights from conversations
- 📝 **Request Logging**: Comprehensive logging of requests and responses
- ⚡ **Fast and Scalable**: Built with FastAPI for high performance
- 🔍 **Health Monitoring**: Detailed component health checks and metrics
- 🔒 **Input Validation**: Robust request validation and error handling

## Quick Start

### Prerequisites

- Python 3.12 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Rihaan-coder/CallChemy.git
cd CallChemy
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the API

Start the FastAPI server:
```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`

### Testing the API

Here are some commands to test the different endpoints:

1. **Check API Status**
```bash
curl http://localhost:8000/
```

2. **Health Check**
```bash
curl http://localhost:8000/health
```

3. **Analyze a Conversation**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "test-001",
    "transcript": [
      {
        "speaker": "Customer",
        "text": "Hi, I am having trouble with my credit card payment."
      },
      {
        "speaker": "Agent",
        "text": "I understand you're having issues with your credit card payment. I'll help you resolve this."
      },
      {
        "speaker": "Customer",
        "text": "Thank you, that would be great!"
      }
    ]
  }'
```

Expected response will include:
- Intent classification for each utterance
- Sentiment analysis scores
- Extracted keywords and topics
- Timestamp of analysis

You can also use tools like [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/) for testing the API with a graphical interface.

### Running Tests

To run the automated test suite:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov

# Run specific test file
pytest tests/test_api.py

# Run tests in verbose mode
pytest -v

# Run tests for a specific component
pytest tests/test_intent_classifier.py -v

# Run tests matching a specific name pattern
pytest -k "test_sentiment"

# Generate HTML coverage report
pytest --cov --cov-report=html
```

The test suite includes:

1. **Unit Tests** (by component):
   - `test_ingestion.py`: Input validation and data structure tests
   - `test_intent_classifier.py`: Intent classification accuracy tests
   - `test_sentiment_analyzer.py`: Sentiment analysis accuracy tests
   - `test_keyword_extractor.py`: Keyword extraction precision tests
   - `test_response_formatter.py`: Response formatting and schema tests
   - `test_logger.py`: Logging functionality and retention tests

2. **Integration Tests** (`test_api.py`):
   - Full API endpoint testing
   - Request/response cycle validation
   - Error handling scenarios
   - Rate limiting and performance tests
   - CORS and security tests

3. **Common Test Scenarios**:
   ```python
   # Example test case from test_intent_classifier.py
   def test_card_issue_intent():
       utterance = "I have a problem with my credit card"
       result = intent_classifier.analyze_text(utterance)
       assert "card_issue" in result.intents
       assert result.confidence > 0.8

   # Example test case from test_sentiment_analyzer.py
   def test_positive_sentiment():
       text = "This service is excellent!"
       result = sentiment_analyzer.analyze_text(text)
       assert result.sentiment == "positive"
       assert result.scores["positive"] > 0.7
   ```

4. **Error Cases**:
   - Invalid input format
   - Missing required fields
   - Malformed JSON
   - Empty transcripts
   - Special characters handling
   - Long text processing
   - Concurrent request handling

5. **Performance Tests**:
   ```bash
   # Run performance tests
   pytest tests/test_api.py -k "test_performance" --durations=0
   ```

6. **Coverage Requirements**:
   - Minimum 80% code coverage
   - All critical paths tested
   - Edge cases covered
   - Error handlers tested

After running tests with coverage, view the HTML report:
```bash
# Generate and open coverage report
pytest --cov --cov-report=html
python -m http.server -d htmlcov 8080
# Open http://localhost:8080 in your browser
```

## API Documentation

Once the server is running, you can access:
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

### Key Endpoints

#### GET /
Root endpoint providing API information and available endpoints.

#### GET /health
Health check endpoint with detailed component status.

#### POST /analyze
Main endpoint for analyzing conversation transcripts.

Example request:
```json
{
    "conversation_id": "conv-123",
    "transcript": [
        {
            "speaker": "Customer",
            "text": "I need help with my credit card."
        },
        {
            "speaker": "Agent",
            "text": "I'll be happy to help you with your credit card issue."
        }
    ]
}
```

Example response:
```json
{
    "conversation_id": "conv-123",
    "timestamp": "2025-07-13T12:00:00Z",
    "analysis": {
        "utterances": [
            {
                "speaker": "Customer",
                "text": "I need help with my credit card.",
                "intent": "card_problem",
                "sentiment": "neutral",
                "keywords": {
                    "financial_terms": [],
                    "products": ["credit card"],
                    "actions": ["help"],
                    "dates": []
                }
            },
            {
                "speaker": "Agent",
                "text": "I'll be happy to help you with your credit card issue.",
                "intent": "customer_service",
                "sentiment": "positive",
                "keywords": {
                    "financial_terms": [],
                    "products": ["credit card"],
                    "actions": ["help"],
                    "dates": []
                }
            }
        ],
        "overall_sentiment": "neutral",
        "primary_intent": "card_problem"
    }
}
```

### Authentication

The `/analyze` endpoint requires an API key. Include it as a query parameter in your requests:

```bash
curl -X POST "http://localhost:8000/analyze?api_key=callchemy-test-key" \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": "test-001", ...}'
```

Note: In production, use a secure API key and set it through environment variables.

## Project Structure

```
CallChemy/
├── api/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and endpoints
│   └── models.py        # Pydantic models for request/response
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── ...
├── ingestion.py         # Input validation
├── intent_classifier.py  # Intent classification logic
├── sentiment_analyzer.py # Sentiment analysis
├── keyword_extractor.py # Keyword extraction
├── response_formatter.py # Response formatting
├── logger.py            # Request logging
└── requirements.txt     # Project dependencies
```

## Error Handling

The API uses standard HTTP status codes:
- 200: Successful request
- 422: Validation error
- 500: Internal server error

All errors return a JSON response with error details:
```json
{
    "detail": "Error message",
    "error_type": "ErrorClassName"
}
```

## Logging

The API logs all requests and responses to:
- `logs/requests.jsonl`: Request/response data
- `logs/backend.log`: System and error logs

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## Contact

Created by [Rihaan-coder](https://github.com/Rihaan-coder)