"""Models for the summarization module."""
from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class SummaryStyle(str, Enum):
    """Available summary styles."""
    BRIEF = "brief"  # Quick overview
    DETAILED = "detailed"  # Comprehensive summary
    ACTION_ITEMS = "action_items"  # Focus on tasks and follow-ups

class SummaryRequest(BaseModel):
    """Request model for conversation summarization."""
    conversation_id: str = Field(..., description="Unique identifier for the conversation")
    utterances: List[Dict[str, str]] = Field(..., description="List of conversation turns")
    style: SummaryStyle = Field(
        default=SummaryStyle.BRIEF,
        description="Style of summary to generate"
    )
    max_length: Optional[int] = Field(
        default=None,
        description="Maximum length of summary in words"
    )
    focus_topics: Optional[List[str]] = Field(
        default=None,
        description="Specific topics to focus on in summary"
    )

class Summary(BaseModel):
    """Response model containing the generated summary."""
    conversation_id: str = Field(..., description="ID of the summarized conversation")
    summary: str = Field(..., description="Generated summary text")
    key_points: List[str] = Field(
        ...,
        description="Main points extracted from conversation"
    )
    action_items: Optional[List[str]] = Field(
        None,
        description="Action items identified in conversation"
    )
    next_steps: Optional[List[str]] = Field(
        None,
        description="Recommended next steps"
    )
    confidence_score: float = Field(
        ...,
        description="Confidence score for summary quality",
        ge=0.0,
        le=1.0
    )
