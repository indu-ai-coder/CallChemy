# Phase 2: Customer-Centric Call Summarization

## Overview

In Phase 2 of the CallChemy project, we enhance the Phase 1 analysis pipeline by introducing **customer-focused summarization**. This summary condenses the core issue, feedback, or resolution from the customer's perspective in one or two concise sentences.

The goal is to provide a quick glance at the conversation's essence—without having to read through every utterance. This is especially useful for post-call analysis, agent coaching, and customer experience audits.

---

## Input

The input format remains the same as in Phase 1—a structured JSON with the following key sections:

- `conversation_id`: Unique identifier for each session.
- `utterances`: List of utterances, each containing:
  - `speaker` (Customer or Agent)
  - `text`
  - `intent`
  - `sentiment`
  - `keywords`

### Example:
```json
{
  "conversation_id": "conv-123",
  "utterances": [
    {
      "speaker": "Customer",
      "text": "I need help with my credit card",
      "intent": "card_problem",
      "sentiment": "neutral",
      "keywords": {
        "financial_terms": [],
        "products": ["card", "credit card"],
        "actions": [],
        "dates": []
      }
    },
    {
      "speaker": "Agent",
      "text": "I'll be happy to help you with that",
      "intent": "no_intent_detected",
      "sentiment": "not_analyzed",
      "keywords": {}
    },
    {
      "speaker": "Customer",
      "text": "Thanks. Glad that issue resolved",
      "intent": "complaint",
      "sentiment": "positive",
      "keywords": {}
    }
  ]
}
```

---

## Output

The response is a JSON structure including everything from Phase 1 along with a new `summary` field.

### Example:
```json
{
  "conversation_id": "conv-123",
  "analysis": {
    "utterances": [...],
    "overall_sentiment": "positive",
    "primary_intent": "complaint"
  },
  "summary": "The customer contacted support regarding a credit card issue, which was resolved satisfactorily.",
  "timestamp": "2025-07-14T11:45:00Z"
}
```

---

## Summary Generation Logic

The summary is generated using an open-source LLM with a **prompt-driven instruction** that ensures:
- Focus only on **Customer** utterances
- Generates **1–2 sentence** summaries
- Maintains a **neutral and professional tone**

If the input contains no customer dialogue, the summary will default to:
```
"Summary not available"
```

---

## Testing

Run the FastAPI server and send a POST request to `/analyze` endpoint:

```bash
curl -X POST http://localhost:8000/analyze      -H "Content-Type: application/json"      -d @sample_input.json
```

The response will now include the `summary` field.

---

## Status

✅ Implemented in `app/summarization.py`  
✅ Integrated into FastAPI pipeline  
✅ Unit tested for different customer dialogue patterns  
🔄 Further refinements will be handled in Phase 3
