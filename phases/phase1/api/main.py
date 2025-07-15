from fastapi import FastAPI, HTTPException, status, Request, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
from .models import ConversationRequest, ConversationResponse

# API Key Settings
API_KEY = "callchemy-test-key"  # In production, use environment variables

def get_api_key(api_key: str = Query(..., description="Your API key")):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Basic"}
        )
    return api_key

from phases.phase1.ingestion import InputValidator
from phases.phase1.intent_classifier import IntentClassifier
from phases.phase1.sentiment_analyzer import SentimentAnalyzer
from phases.phase1.keyword_extractor import KeywordExtractor
from phases.phase1.response_formatter import ResponseFormatter
from phases.phase1.logger import CallChemyLogger
from datetime import datetime, timezone


# Global variable to track API startup time
startup_time = datetime.now(timezone.utc)

app = FastAPI(
    title="CallChemy API",
    description="Conversation Analysis Pipeline",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Changed to False for testing
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
input_validator = InputValidator()
intent_classifier = IntentClassifier()
sentiment_analyzer = SentimentAnalyzer()
keyword_extractor = KeywordExtractor()
response_formatter = ResponseFormatter()
logger = CallChemyLogger()

@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup"""
    global startup_time
    startup_time = datetime.now(timezone.utc)
    logger.log_request(
        conversation_id="system",
        request_data={"event": "startup"},
        response_data={"status": "API initialized"}
    )

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown"""
    logger.log_request(
        conversation_id="system",
        request_data={"event": "shutdown"},
        response_data={"status": "API shutdown"}
    )

@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint that provides API information and available endpoints.
    """
    return {
        "name": "CallChemy API",
        "version": "1.0.0",
        "description": "Conversation Analysis Pipeline for Customer Service Interactions",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "analyze": "/analyze"
        },
        "features": [
            "Intent Classification",
            "Sentiment Analysis",
            "Keyword Extraction",
            "Conversation Summarization"
        ],
        "status": "operational"
    }

@app.get("/health", tags=["System"])
async def health_check(request: Request):
    """
    Health check endpoint that provides detailed system component status
    """
    try:
        components_status = {}
        start_time = datetime.now(timezone.utc)
        
        # Test Input Validator
        try:
            test_data = {
                "transcript": [
                    {"speaker": "Customer", "text": "Test message"}
                ]
            }
            input_validator.validate(test_data)
            end_time = datetime.now(timezone.utc)
            components_status["input_validator"] = {
                "status": "operational",
                "latency_ms": round((end_time - start_time).total_seconds() * 1000)
            }
        except Exception as e:
            components_status["input_validator"] = {"status": "error", "message": str(e)}

        # Test Intent Classifier
        try:
            start_time = datetime.now(timezone.utc)
            test_utterances = [{"text": "I need help with my card", "speaker": "Customer"}]
            intent_classifier.analyze_transcript(test_utterances)
            end_time = datetime.now(timezone.utc)
            components_status["intent_classifier"] = {
                "status": "operational",
                "latency_ms": round((end_time - start_time).total_seconds() * 1000)
            }
        except Exception as e:
            components_status["intent_classifier"] = {"status": "error", "message": str(e)}

        # Test Sentiment Analyzer
        try:
            start_time = datetime.now(timezone.utc)
            test_utterances = [{"text": "This is great service", "speaker": "Customer"}]
            sentiment_analyzer.analyze_transcript(test_utterances)
            end_time = datetime.now(timezone.utc)
            components_status["sentiment_analyzer"] = {
                "status": "operational",
                "latency_ms": round((end_time - start_time).total_seconds() * 1000)
            }
        except Exception as e:
            components_status["sentiment_analyzer"] = {"status": "error", "message": str(e)}

        # Test Keyword Extractor
        try:
            start_time = datetime.now(timezone.utc)
            test_utterances = [{"text": "My credit card is blocked", "speaker": "Customer"}]
            keyword_extractor.analyze_transcript(test_utterances)
            end_time = datetime.now(timezone.utc)
            components_status["keyword_extractor"] = {
                "status": "operational",
                "latency_ms": round((end_time - start_time).total_seconds() * 1000)
            }
        except Exception as e:
            components_status["keyword_extractor"] = {"status": "error", "message": str(e)}

        # Test Response Formatter
        try:
            start_time = datetime.now(timezone.utc)
            test_data = {
                "conversation_id": "test-123",
                "utterances": [{"text": "Test", "speaker": "Customer"}]
            }
            response_formatter.format_response(**test_data)
            end_time = datetime.now(timezone.utc)
            components_status["response_formatter"] = {
                "status": "operational",
                "latency_ms": round((end_time - start_time).total_seconds() * 1000)
            }
        except Exception as e:
            components_status["response_formatter"] = {"status": "error", "message": str(e)}

        # Test Logger
        try:
            start_time = datetime.now(timezone.utc)
            logger.log_request("test-123", {"test": "data"})
            end_time = datetime.now(timezone.utc)
            components_status["logger"] = {
                "status": "operational",
                "latency_ms": round((end_time - start_time).total_seconds() * 1000)
            }
        except Exception as e:
            components_status["logger"] = {"status": "error", "message": str(e)}
        
        system_status = all(
            comp.get("status") == "operational" 
            for comp in components_status.values()
        )
        
        return {
            "status": "healthy" if system_status else "degraded",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "components": components_status,
            "api_version": "1.0.0",
            "uptime_seconds": round((datetime.now(timezone.utc) - startup_time).total_seconds())
        }
    except Exception as e:
        logger.log_request(
            conversation_id="system",
            request_data={"path": str(request.url)},
            error=e
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"}
        )

@app.post("/analyze", response_model=ConversationResponse)
async def analyze_conversation(
    request: ConversationRequest,
    api_key: str = Depends(get_api_key)
) -> ConversationResponse:
    """
    Analyze a conversation transcript and return structured insights.
    
    Args:
        request (ConversationRequest): The conversation request containing transcript
        
    Returns:
        ConversationResponse: Analysis results including intents, sentiment, and keywords
        
    Raises:
        HTTPException: 422 for validation errors, 500 for internal errors
    """
    try:
        # Validate request
        if not request.transcript:
            raise ValueError("Transcript cannot be empty")
            
        # Validate input structure
        validated_data = input_validator.validate(request.dict())
        
        # Run analysis pipeline
        with_intents = intent_classifier.analyze_transcript(validated_data["transcript"])
        with_sentiment = sentiment_analyzer.analyze_transcript(with_intents)
        with_keywords = keyword_extractor.analyze_transcript(with_sentiment)
        
        # Format response
        response = response_formatter.format_response(
            conversation_id=request.conversation_id,
            utterances=with_keywords
        )
        
        # Log successful request
        logger.log_request(
            conversation_id=request.conversation_id,
            request_data=request.dict(),
            response_data=response
        )
        
        return response
    except Exception as e:
        logger.log_request(
            conversation_id=request.conversation_id,
            request_data=request.dict(),
            error=e
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error", "error_type": type(e).__name__}
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    logger.log_request(
        conversation_id="system",
        request_data={"path": str(request.url)},
        error=exc
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )