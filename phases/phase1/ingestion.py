from pydantic import BaseModel, Field
from typing import List, Dict

class Utterance(BaseModel):
    speaker: str = Field(..., pattern="^(Customer|Agent)$")
    text: str = Field(..., min_length=1)

class Transcript(BaseModel):
    conversation_id: str
    transcript: List[Dict[str, str]]

class InputValidator:
    def validate(self, data: Dict) -> Dict:
        """Validate input transcript data"""
        try:
            # Validate basic structure
            validated = Transcript(**data)
            
            # Validate each utterance
            for idx, utterance in enumerate(validated.transcript):
                Utterance(**utterance)
                
            return validated.model_dump()  # Updated to use model_dump() instead of dict()
            
        except Exception as e:
            raise ValueError(f"Validation error at index {idx}: {str(e)}")