from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, status, Request, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .models import ConversationRequest, ConversationResponse
from phases.phase2.ingestion import InputValidator
from phases.phase2.intent_classifier import IntentClassifier
from phases.phase2.sentiment_analyzer import SentimentAnalyzer
from phases.phase2.keyword_extractor import KeywordExtractor
from phases.phase2.response_formatter import ResponseFormatter
from phases.phase2.logger import CallChemyLogger

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown events"""
    # Startup: Initialize resources
    logger.log_request(
        conversation_id="system",
        request_data={"event": "startup"},
        response_data={"status": "API initialized"}
    )
    yield
    # Shutdown: Cleanup resources
    logger.log_request(
        conversation_id="system",
        request_data={"event": "shutdown"},
        response_data={"status": "API shutdown"}
    )

app = FastAPI(
    title="CallChemy API",
    description="Conversation Analysis Pipeline",
    version="1.0.0",
    lifespan=lifespan
)

# Initialize components
input_validator = InputValidator()
intent_classifier = IntentClassifier()
sentiment_analyzer = SentimentAnalyzer()
keyword_extractor = KeywordExtractor()
response_formatter = ResponseFormatter()
logger = CallChemyLogger()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"]
)

@app.options("/{path:path}")
async def options_handler(path: str):
    """Handle CORS preflight requests"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )

@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint that provides API information and available endpoints.
    """
    return {
        "title": "CallChemy API",
        "version": "1.0.0",
        "description": "Conversation Analysis Pipeline for Customer Service Interactions",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "analyze": "/analyze"
        },
        "status": "operational"
    }

@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

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
        validated_data = input_validator.validate(request.model_dump())
        
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
            request_data=request.model_dump(),
            response_data=response
        )
        
        return response
    except ValueError as e:
        logger.log_request(
            conversation_id=request.conversation_id,
            request_data=request.model_dump(),
            error=e
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": str(e)}
        )
    except Exception as e:
        logger.log_request(
            conversation_id=request.conversation_id,
            request_data=request.model_dump(),
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