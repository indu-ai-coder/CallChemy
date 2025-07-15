
# 📞 CallChemy - Specification

**Project Purpose**:  
CallChemy is an API-powered system that processes transcribed customer-agent conversations and turns them into structured insights. It extracts **intents**, **customer sentiment**, **key phrases**, and **summaries** — delivering clear, actionable intelligence for QA and analytics teams.

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
