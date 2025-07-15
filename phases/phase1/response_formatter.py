from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone
from pydantic.json_schema import JsonSchemaMode

class UtteranceAnalysis(BaseModel):
    speaker: str
    text: str
    intent: Optional[str] = None
    sentiment: Optional[str] = None
    keywords: Optional[Dict[str, List[str]]] = None

class CallSummary(BaseModel):
    paragraph: str
    bullet_points: List[str]

class AnalysisResponse(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_default=True
    )
    
    conversation_id: str
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        json_schema_extra={'format': 'date-time'}
    )
    utterances: List[UtteranceAnalysis]
    summary: Optional[CallSummary] = None
    overall_sentiment: Optional[str] = None
    primary_intent: Optional[str] = None
    key_findings: Dict[str, List[str]] = Field(default_factory=dict)

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data['timestamp'] = data['timestamp'].isoformat()
        return data

class ResponseFormatter:
    def __init__(self):
        self.fallback_values = {
            'intent': 'no_intent_detected',
            'sentiment': 'not_analyzed',
            'keywords': {'financial_terms': [], 'products': [], 'actions': []}
        }

    def _get_overall_sentiment(self, utterances: List[Dict]) -> str:
        """Calculate overall sentiment from customer utterances"""
        customer_sentiments = [
            u.get('sentiment') for u in utterances 
            if u['speaker'] == "Customer" and u.get('sentiment') != "not_analyzed"
        ]
        if not customer_sentiments:
            return "neutral"
        
        sentiment_counts = {
            'positive': customer_sentiments.count('positive'),
            'negative': customer_sentiments.count('negative'),
            'neutral': customer_sentiments.count('neutral')
        }
        return max(sentiment_counts, key=sentiment_counts.get)

    def _get_primary_intent(self, utterances: List[Dict]) -> str:
        """Determine primary intent from customer utterances"""
        customer_intents = [
            u.get('intent') for u in utterances
            if u['speaker'] == "Customer" and u.get('intent') != "no_intent_detected"
        ]
        if not customer_intents:
            return "no_intent_detected"
        return max(set(customer_intents), key=customer_intents.count)

    def format_response(self, 
                       conversation_id: str,
                       utterances: List[Dict],
                       summary: Optional[Dict] = None) -> Dict:
        """Format analysis results into final API response"""
        formatted_utterances = [
            UtteranceAnalysis(
                speaker=u['speaker'],
                text=u['text'],
                intent=u.get('intent', self.fallback_values['intent']),
                sentiment=u.get('sentiment', self.fallback_values['sentiment']),
                keywords=u.get('keywords', self.fallback_values['keywords'])
            ) for u in utterances
        ]
        
        overall_sentiment = self._get_overall_sentiment(utterances)
        primary_intent = self._get_primary_intent(utterances)
        
        response = {
            "conversation_id": conversation_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "analysis": {
                "utterances": [u.model_dump() for u in formatted_utterances],
                "overall_sentiment": overall_sentiment,
                "primary_intent": primary_intent
            }
        }
        
        if summary:
            response["analysis"]["summary"] = summary
            
        return response