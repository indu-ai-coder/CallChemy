![CallChemy Banner](docs/callchemy-banner.png)

# 📞 CallChemy – AI-powered Call Summary and Quality Analyzer

**CallChemy** is an LLM-powered backend system designed to analyze transcribed customer-agent conversations and extract actionable insights — such as intent, sentiment, and call summaries. The project is built in modular phases to allow experimentation and iterative improvement.

---

## 🧠 What Can CallChemy Do?

Given a transcribed audio conversation (e.g., from a call center), CallChemy can:
- Detect customer **intents** (e.g., complaint, inquiry, feedback)
- Analyze **sentiment** (positive, negative, neutral)
- Extract **keywords** (products, dates, financial terms)
- Generate a **structured analysis report**
- (Phase 2) Generate a summary and enable **interactive dashboarding**

---

## 🧩 Project Structure

```
CallChemy/
├── phases/
│   ├── phase1/         # Static analysis via API (intent, sentiment, keywords)
│   └── phase2/         # (Upcoming) Summary generation, dashboard integration
├── docs/               # Architecture, screenshots, planning artifacts
├── README.md           # You are here
└── prompt_plan.md      # Spec-first development tracker
```

📌 Each phase has its own `README.md` with:
- Setup instructions  
- API examples  
- Expected input/output  
- Future TODOs

---

## ⚙️ Tech Stack

| Area | Tools |
|------|-------|
| 💬 LLMs | Claude, OpenAI (Optional), open-source LLMs (planned in Phase 2) |
| 🧠 Prompt Workflow | Specification-grounded development (`idea.md`, `spec.md`, `prompt_plan.md`) |
| 🧪 Backend | FastAPI |
| ⚙️ Dev Tools | GitHub Copilot, Claude, Postman |
| ☁️ Future (optional) | Streamlit, LangChain, Hugging Face Hub |

---

## 🚀 Getting Started

### 🛠 Requirements
- Python 3.10+
- `pip install -r requirements.txt` (per phase folder)
- (Optional) Claude or OpenAI keys for Phase 2

### ▶️ Run Phase 1 API Locally

```bash
cd phases/phase1
uvicorn main:app --reload
```

Then test the `/analyze` endpoint using Postman or curl.

---

## 📖 Development Approach

This project uses a **spec-driven, prompt-first development methodology** inspired by the [Unstract](https://unstract.com/blog/specification-grounding-vibe-coding/) framework:

- Define the vision → `idea.md`
- Lock down inputs/outputs → `spec.md`
- Break dev into steps → `prompt_plan.md`
- Guide the loop with Claude → `CLAUDE.md`

This makes the AI + API build process predictable, repeatable, and testable.

---

## ✍️ Author

**Indumathi Pandiyan**  
AI Enthusiast | Techpreneur | Conversational AI Architect  
[LinkedIn](https://www.linkedin.com/in/indumathi-pandiyan/) | [Medium](https://medium.com/@indukishen)

---

## ⭐️ Acknowledgments

- [Unstract](https://github.com/zipstack/unstract) for spec-grounded development approach
- [Shuveb Hussain](https://github.com/shuveb) for inspiring builder culture
- The **Saama AI** community for sparking the build momentum during the July meetup

---

## 🛤️ Roadmap

- [x] Phase 1: Intent + Sentiment + API complete
- [ ] Phase 2: Add summary generation with LLM
- [ ] Phase 2: Interactive dashboard (e.g., Streamlit)
- [ ] Phase 3: Add multi-language support (e.g., Tamil, Hindi)
- [ ] Phase 4: Real-time audio ingestion + diarization

---

## 📬 Want to Collaborate or Contribute?

Feel free to open an issue, drop feedback, or reach out on LinkedIn.  
Together, we can make CallChemy an open blueprint for practical LLM apps in customer experience and QA.
