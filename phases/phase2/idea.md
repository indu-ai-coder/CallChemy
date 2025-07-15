
# 🎯 Phase 2: LLM-Powered Conversation Summarization

## 💡 Vision
Extend CallChemy to provide high-quality, actionable conversation summaries using LLMs. Phase 2 focuses on generating meaningful summaries that capture key points, action items, and next steps while maintaining Phase 1's modular architecture.

## 🎯 Goal
To develop a lightweight MVP that enables businesses to:
- Automatically extract **intent** from user utterances.
- Detect **customer sentiment** across the conversation.
- Generate a **text summary** of the conversation.
- Produce **structured output** (JSON, CSV) suitable for analytics or QA review.

## 👥 Users
- **Customer Support QA Teams**
- **Product Managers** evaluating customer feedback
- **Startups** needing quick analysis of user call logs

## ⚙️ Key Features
1. **Transcript Ingestion via API** – Accept a POST request containing a structured transcript (speaker + text).
2. **Intent Classification** – Tag utterances with one or more of 6 predefined intents.
3. **Sentiment Detection** – Classify each user message and/or entire conversation as Positive, Negative, or Neutral.
4. **Conversation Summary** – Extractive or abstractive summary of the conversation.
5. **Static Report Generator** – Output results to CSV or JSON.
6. **Spec-Grounded Prompting** – Every model/prompt module is preceded by a clarifying spec and prompt plan.

## 🧩 MVP Assumptions
- Input: Transcribed text only (for now), received via REST API
- Language: English
- Speakers: Only Agent and Customer
- Output: Static structured report (JSON/CSV)
- Phase 2: Add audio-to-text and interactive dashboard

## 🌐 Input/Output API Structure

**Endpoint:** `POST /analyze`

**Sample Input JSON:**
```json
{
  "conversation_id": "ABC123",
  "transcript": [
    { "speaker": "Customer", "text": "I didn’t receive my refund." },
    { "speaker": "Agent", "text": "Let me check your account." }
  ]
}
```

**Sample Output JSON:**
```json
{
  "conversation_id": "ABC123",
  "summary": "Customer complained about a missing refund. Agent investigated the issue.",
  "customer_sentiment": "negative",
  "intents_detected": ["complaint", "follow-up"],
  "output_format": "json"
}
```

## 🖼️ Future UI Ideas (Post-MVP)
- Transcript viewer with highlighted intents
- Sentiment timeline
- Filterable dashboard by intent/sentiment

## 🤖 Rubber Duck Setting
Before coding, every component will be preceded by:
- A clarified prompt + schema spec
- Sample inputs/outputs
- Edge case reasoning
This allows us to debug *intent* before debugging code.
