from typing import List, Dict
import re

class IntentClassifier:
    def __init__(self):
        self.intent_patterns = {
            'account_inquiry': r'\b(account|balance|statement|transactions|history)\b',
            'transaction_issue': r'\b(transfer|payment|deposit|withdraw|transaction)\b',
            'card_problem': r'\b(card|pin|atm|blocked|decline)\b',
            'loan_request': r'\b(loan|emi|interest|borrowing|mortgage)\b',
            'complaint': r'\b(problem|issue|complaint|wrong|error|dispute)\b',
            'follow_up': r'\b(status|update|when|follow|pending)\b'
        }

    def classify_utterance(self, text: str) -> str:
        """
        Classify a single utterance into an intent category.
        Returns: one of the defined intents or 'no_intent_detected'
        """
        text = text.lower()
        
        # Skip very short greetings/thanks
        if len(text.split()) <= 2 and re.search(r'\b(hi|hello|thanks|thank you)\b', text):
            return 'no_intent_detected'
            
        # Check each intent pattern
        for intent, pattern in self.intent_patterns.items():
            if re.search(pattern, text):
                return intent
                
        return 'no_intent_detected'

    def analyze_transcript(self, utterances: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Analyze all utterances in the transcript and add intent classification.
        Returns: Original utterances with added 'intent' field
        """
        return [
            {**utterance, 'intent': self.classify_utterance(utterance['text'])}
            for utterance in utterances
        ]