
# 🧩 CallChemy Prompt Plan  
**Version:** v0.1  
**Created:** 2025-07-13  
**Owner:** Indumathi  
**Stack:** Python 3.11, FastAPI, Pydantic, pytest, basic NLP tools

---

## ✅ Module Implementation Tracker

| Step | Module / File         | Task Description                            | Status   |
|------|------------------------|---------------------------------------------|----------|
| 1    | ingestion.py           | Validate and parse input transcript JSON    | 🔜 Pending |
| 2    | intent_classifier.py   | Classify intent from each utterance         | 🔜 Pending |
| 3    | sentiment_analyzer.py  | Detect sentiment of customer utterances     | 🔜 Pending |
| 4    | summary_generator.py   | Generate paragraph and bullet-point summary | 🔜 Pending |
| 5    | keyword_extractor.py   | Extract key terms and entities              | 🔜 Pending |
| 6    | response_formatter.py  | Combine module results into final response  | 🔜 Pending |
| 7    | logger.py              | Log inputs/outputs to file system           | 🔜 Pending |
| 8    | api/main.py            | Create FastAPI app with single endpoint     | 🔜 Pending |

---

## 🧩 Detailed Steps

### ✅ **1. ingestion.py** – Input validation module [Status: Done]
- Use Pydantic to validate:
  - `conversation_id`: string, required
  - `transcript`: list of objects with:
    - `speaker`: must be "Customer" or "Agent"
    - `text`: non-empty string
- Return 422 errors with index & helpful message
- Reject malformed JSON with structured response

🧪 Tests:
- [x] Valid input (200)
- [x] Missing fields
- [x] Invalid speaker
- [x] Empty transcript

---

### 🔜 **2. intent_classifier.py** – Intent Detection [Status: Pending]
- Accepts list of utterances, classifies each into one of:
  - `account_inquiry`, `transaction_issue`, `card_problem`, `loan_request`, `complaint`, `follow_up`, `no_intent_detected`
- Use keyword-based rule matcher (initial)
- Plan for open-source LLM upgrade in Phase 2

🧪 Tests:
- [ ] One-liner classifier test
- [ ] Edge case: greetings/thanks
- [ ] Multiple intents (simulate but flag one)

---

### 🔜 **3. sentiment_analyzer.py** – Customer Sentiment [Status: Pending]
- Only analyze `Customer` utterances
- Labels: `positive`, `neutral`, `negative`
- Use VADER/TextBlob or open-source LLM later

🧪 Tests:
- [ ] Negative complaint
- [ ] Neutral query
- [ ] Polite positive statement

---

### 🔜 **4. summary_generator.py** – Summarization [Status: Pending]
- Generate both:
  - Short paragraph summary
  - Bullet-point breakdown
- Use simple extractive logic first, upgrade to BART/T5 if needed

🧪 Tests:
- [ ] Basic refund complaint summary
- [ ] Card blocked resolution
- [ ] Summary with mixed tones

---

### 🔜 **5. keyword_extractor.py** – Key Phrases [Status: Pending]
- Extract:
  - Financial terms (e.g., ₹5000, refund, EMI)
  - Product names (card, loan)
  - Actions/issues (blocked, delayed)
- Use regex + SpaCy or YAKE

🧪 Tests:
- [ ] Transaction issue phrase
- [ ] Date/time entity
- [ ] Multilingual token (ignore or flag)

---

### 🔜 **6. response_formatter.py** – Output Packager [Status: Pending]
- Assemble:
  - Intent, sentiment, keywords, summary
  - Into API-ready JSON structure
- Add fallback fields for missing items

🧪 Tests:
- [ ] All modules filled
- [ ] Some modules skipped
- [ ] Output field schema validation

---

### 🔜 **7. logger.py** – Request/Response Logger [Status: Pending]
- Save each request & result to:
  - JSONL file or SQLite table
- Include timestamp, conversation ID, result snapshot
- Add optional retention config

🧪 Tests:
- [ ] Log success
- [ ] Log error with traceback
- [ ] Configurable path

---

### 🔜 **8. api/main.py** – FastAPI Endpoint [Status: Pending]
- `POST /analyze` route
- Accepts input JSON, runs full pipeline
- Returns full output JSON or error
- Auto docs enabled (`/docs`)

🧪 Tests:
- [ ] Happy path
- [ ] 422 failure (bad input)
- [ ] Full pipeline test

---

> 🧠 Use this plan to drive modular LLM development.  
> After each step is completed, mark the `Status` as ✅ Done.
