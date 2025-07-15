# CallChemy 🧪

A powerful conversation analysis platform that turns customer service interactions into actionable insights through advanced NLP.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green.svg)

## 🌟 Overview

CallChemy is an intelligent conversation analysis API that helps businesses understand and improve their customer service interactions. Using state-of-the-art natural language processing, it extracts meaningful insights from conversations, including:

- Intent Classification
- Sentiment Analysis
- Keyword Extraction
- Conversation Summarization

## 📚 Project Structure

CallChemy is organized into phases, each building upon the previous:

### [Phase 1](/phases/phase1/) - Core API
- FastAPI-based REST API
- Basic NLP pipeline
- Input validation
- Request logging
- [Detailed Documentation](/phases/phase1/README.md)

*Future phases will be added as the project evolves.*

## 🚀 Quick Start

1. **Prerequisites**
   - Python 3.12+
   - pip (Python package installer)

2. **Installation**
   ```bash
   git clone https://github.com/indu-ai-coder/CallChemy.git
   cd CallChemy
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r phases/phase1/requirements.txt
   ```

3. **Run the API**
   ```bash
   uvicorn phases.phase1.api.main:app --reload
   ```

   Visit `http://localhost:8000/docs` for interactive API documentation.

## 💡 Key Features

- 🎯 **Smart Intent Detection**: Accurately identifies customer needs and conversation goals
- 😊 **Sentiment Tracking**: Monitors emotional tone and satisfaction levels
- 🔑 **Key Topic Extraction**: Identifies important subjects and action items
- 📊 **Structured Insights**: Converts raw conversations into actionable data
- ⚡ **High Performance**: Built for speed and scalability
- 🔒 **Robust Validation**: Comprehensive input validation and error handling

## 🛠️ Development

Each phase has its own test suite and documentation. See individual phase READMEs for detailed development guidelines.

```bash
# Run tests for current phase
pytest phases/phase1/tests/

# Run with coverage
pytest phases/phase1/tests/ --cov
```

## 📖 Documentation

- [Phase 1 Documentation](/phases/phase1/README.md)
- API Documentation (when server is running):
  - Swagger UI: `http://localhost:8000/docs`
  - ReDoc: `http://localhost:8000/redoc`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contact

Created by [indu-ai-coder](https://github.com/indu-ai-coder)

---
⭐ Star us on GitHub — it motivates us to keep improving!
