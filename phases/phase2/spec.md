
# Phase 2: LLM-Powered Summarization Specification

**Phase Purpose**:  
Phase 2 extends CallChemy with advanced summarization capabilities, using LLMs to generate high-quality, actionable summaries from customer-agent conversations. It builds on Phase 1's analysis features while adding robust summarization that captures key points, action items, and next steps.

## Core Requirements

### 1. Summary Generation
- Generate coherent, contextual summaries
- Support multiple summary styles (brief, detailed, action-focused)
- Extract key points and action items
- Provide confidence scores
- Handle multi-turn context

### 2. LLM Integration
- Primary: Claude API integration
- Fallback: Local model support
- Extensible provider system
- Async processing
- Error handling and retries

### 3. API Enhancement
- New /v2/summarize endpoint
- Enhanced /v2/analyze endpoint
- Backward compatibility
- Proper error responses

## Technical Specifications

### Data Models
```python
# Summary Request
{
    "conversation_id": str,
    "utterances": List[Dict[str, str]],
    "style": Enum["brief", "detailed", "action_items"],
    "max_length": Optional[int],
    "focus_topics": Optional[List[str]]
}

# Summary Response
{
    "conversation_id": str,
    "summary": str,
    "key_points": List[str],
    "action_items": Optional[List[str]],
    "next_steps": Optional[List[str]],
    "confidence_score": float
}
```

### Performance Requirements
- Response time < 2 seconds
- 99.9% API availability
- Graceful degradation
- Efficient caching

### Quality Metrics
- Summary relevance score
- Action item accuracy
- Key point coverage
- Grammar and coherence

---

## 🚀 MVP Scope (Phase 1)

### ✅ Input
- Format: JSON
- Required fields:
  - `conversation_id`: unique ID
  - `transcript`: list of utterances
    - Each utterance includes:
      - `speaker`: must be "Agent" or "Customer"
      - `text`: the spoken sentence or phrase
- Multiple consecutive utterances by the same speaker are supported

**Example Input:**
```json
{
  "conversation_id": "ABC123",
  "transcript": [
    { "speaker": "Customer", "text": "I didn’t receive my refund." },
    { "speaker": "Agent", "text": "Let me check your account." }
  ]
}
```

---

### 📤 Output
- Returned directly via API response (JSON)
- Includes:
  - `summary`: short paragraph or bullet points (whichever performs better)
  - `customer_sentiment`: overall tone
  - `utterance_analysis`: intent + sentiment per utterance
  - `keywords`: relevant entities extracted
  - `intents`: top-level intents mentioned in conversation

**Example Output:**
```json
{
  "conversation_id": "ABC123",
  "summary": "Customer reported a blocked card. Agent initiated re-issuance.",
  "customer_sentiment": "negative",
  "utterance_analysis": [
    {
      "speaker": "Customer",
      "text": "This is taking forever!",
      "intent": "complaint",
      "sentiment": "negative"
    },
    {
      "speaker": "Agent",
      "text": "Let me help you with that.",
      "intent": "assistance",
      "sentiment": null
    }
  ],
  "keywords": ["blocked card", "refund", "₹5000"],
  "intents": ["complaint", "card_problem"]
}
```

---

## 🧠 Intent Categories (Banking Domain)
- `account_inquiry`: balance, type, or status
- `transaction_issue`: unauthorized or missing transaction
- `card_problem`: lost, stolen, or blocked cards
- `loan_request`: apply, check status, EMI info
- `complaint`: general dissatisfaction
- `follow_up`: returning to a previously reported issue
- `no_intent_detected`: for greetings, confirmations, etc.

---

## 🧪 Sentiment Detection
- Applied **only to Customer utterances**
- Labels: `positive`, `neutral`, `negative`

---

## 🧬 Summary Generation
- Two styles: paragraph or bullet points
- Return best based on performance and clarity

---

## 🧷 Keyword/Entity Extraction
- Use NLP tools (e.g., SpaCy or Transformers) to extract:
  - Product types
  - Monetary values
  - Dates/times
  - Actions/issues

---

## 🛠️ Architecture
- Modular design using **FastAPI** and components:
  - `ingestion.py`: validate inputs
  - `intent_classifier.py`
  - `sentiment_analyzer.py`
  - `summary_generator.py`
  - `keyword_extractor.py`
  - `response_formatter.py`
  - `logger.py`: for saving inputs + outputs

---

## 🧠 Model Choice
- Use **open-source LLMs** (e.g., Mistral, OpenChat, Phi) for:
  - Intent classification
  - Summary generation
- Rule-based or classical ML fallback for keywords

---

## ⚙️ Error Handling
- Structured developer-friendly messages
- Example:
```json
{
  "status": 422,
  "error": "Invalid speaker field at index 4",
  "suggestion": "Speaker must be 'Agent' or 'Customer'"
}
```

---

## 🔐 Authentication
- None in Phase 1
- Phase 2: API keys or token-based access

---

## 🧾 Logging
- Each request and response saved for review and model retraining
- Format: JSONL or SQLite
- Stored under `/logs/` or `/data/processed/`

---

## 📦 Deployment Plan (Phase 1)
- Run locally via FastAPI (`uvicorn`)
- No dashboard/UI yet
- API only

---

## 🛣️ Future Roadmap (Phase 2)
- Batch input support
- Interactive UI (Streamlit or React)
- File upload/download (CSV, JSON)
- Dashboard with filtering and charts
- Cloud deployment (Render, GCP, AWS)

---

## 🧪 Testing Suggestions
- Unit tests for each module
- Sample payloads to test summary, intent, and sentiment modules

---

Project Codename: **CallChemy 🔮**
