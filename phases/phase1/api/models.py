from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ConversationRequest(BaseModel):
    conversation_id: str = Field(..., min_length=1, description="Unique conversation identifier")
    transcript: List[Dict[str, str]] = Field(..., min_items=1, description="List of utterances with speaker and text")

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "conv-123",
                "transcript": [
                    {"speaker": "Customer", "text": "I need help with my credit card"},
                    {"speaker": "Agent", "text": "I'll be happy to help you with that"}
                ]
            }
        }

class ConversationResponse(BaseModel):
    conversation_id: str
    analysis: Dict = Field(..., description="Analysis results including intents, sentiment, and keywords")
    summary: Optional[Dict[str, List[str]]] = Field(None, description="Conversation summary and key points")
    timestamp: str = Field(..., description="Analysis timestamp in ISO format")

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "conv-123",
                "timestamp": "2025-07-13T14:30:00Z",
                "analysis": {
                    "primary_intent": "card_problem",
                    "overall_sentiment": "neutral",
                    "utterances": [
                        {
                            "speaker": "Customer",
                            "text": "I need help with my credit card",
                            "intent": "card_problem",
                            "sentiment": "neutral",
                            "keywords": {
                                "products": ["credit card"]
                            }
                        }
                    ]
                },
                "summary": {
                    "key_points": ["Customer requested credit card assistance"]
                }
            }
        }