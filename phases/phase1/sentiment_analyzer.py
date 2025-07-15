from typing import List, Dict
from textblob import TextBlob

class SentimentAnalyzer:
    def __init__(self):
        self.sentiment_thresholds = {
            'positive': 0.1,
            'negative': -0.1
        }

    def analyze_utterance(self, text: str) -> str:
        """
        Analyze sentiment of a single utterance using TextBlob.
        Returns: 'positive', 'neutral', or 'negative'
        """
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity

        if polarity >= self.sentiment_thresholds['positive']:
            return 'positive'
        elif polarity <= self.sentiment_thresholds['negative']:
            return 'negative'
        return 'neutral'

    def analyze_transcript(self, utterances: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Analyze sentiment for customer utterances in the transcript.
        Returns original utterances with added sentiment field.
        """
        analyzed = []
        for utterance in utterances:
            # Only analyze customer utterances
            sentiment = self.analyze_utterance(utterance['text']) if utterance['speaker'] == 'Customer' else 'not_analyzed'
            analyzed.append({
                **utterance,
                'sentiment': sentiment
            })
        return analyzed