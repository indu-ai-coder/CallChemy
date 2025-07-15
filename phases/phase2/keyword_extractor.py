from typing import List, Dict, Set
import re

class KeywordExtractor:
    def __init__(self):
        self.financial_patterns = {
            'amount': r'(?:₹|Rs\.?|INR)\s*\d+(?:,\d+)*(?:\.\d{2})?',
            'percentage': r'\d+(?:\.\d+)?%',
            'account': r'\b(?:account|a/c)\s*#?\s*\d+\b',
            'card': r'\b(?:card|credit|debit)\s*#?\s*\d+\b'
        }
        
        self.product_terms = {
            'card': {'credit card', 'debit card', 'atm card', 'card'},
            'loan': {'personal loan', 'home loan', 'car loan', 'emi', 'mortgage'},
            'account': {'savings', 'current', 'fd', 'fixed deposit'}
        }
        
        self.action_terms = {
            'blocked', 'delayed', 'failed', 'declined', 'expired',
            'pending', 'rejected', 'approved', 'processed'
        }

    def extract_keywords(self, text: str) -> Dict[str, List[str]]:
        """Extract keywords and entities from text"""
        keywords = {
            'financial_terms': [],
            'products': [],
            'actions': [],
            'dates': []
        }
        
        # Extract financial terms using regex
        for label, pattern in self.financial_patterns.items():
            matches = re.finditer(pattern, text)
            keywords['financial_terms'].extend([m.group() for m in matches])
        
        # Extract products
        text_lower = text.lower()
        for category, terms in self.product_terms.items():
            for term in terms:
                if term in text_lower:
                    keywords['products'].append(term)
        
        # Extract actions
        for action in self.action_terms:
            if action in text_lower:
                keywords['actions'].append(action)
        
        # Remove duplicates while preserving order
        return {k: list(dict.fromkeys(v)) for k, v in keywords.items()}

    def analyze_transcript(self, utterances: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Analyze all utterances and extract keywords"""
        return [
            {**utterance, 'keywords': self.extract_keywords(utterance['text'])}
            for utterance in utterances
        ]