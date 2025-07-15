# 🤖 CLAUDE.md – LLM-Driven Dev Plan for CallChemy
## 📦 Project: CallChemy – Call Summary & Quality Analyzer
This is a structured LLM-driven development session to implement an MVP using modular steps.

---

## 🧾 Context Files to Load

The following files should be fully read into context:

- `idea.md` → Overview, product goals, scope  
- `spec.md` → Detailed input/output formats, architecture, assumptions  
- `prompt_plan.md` → Step-by-step implementation guide  

---

Always read and follow these files closely before starting development on any module.

After implementing any module:
- Write and verify appropriate test cases.
- Confirm the output aligns with the spec.
- Mark the step as `Done` in `prompt_plan.md` before moving to the next.

---

## 🛠️ System & Development Notes

- This project uses **FastAPI**, which will be started manually by the user.
- Logs will be written to `logs/backend.log`.
- Do **not start the FastAPI server yourself**; I will run it manually.
- Always ensure your code writes clean logs and errors to `logs/backend.log`.

---

## 🐍 Virtual Environment

- Use the `venv/` folder in the project root.
- Never use the system Python.
- Install all dependencies using `pip install -r requirements.txt`.

---

## ✅ Git Commit Policy

- Only commit or push code after **explicit confirmation from me**.
- Always commit from the project root.
- Avoid auto-generating `.gitignore`, `.env`, or `.DS_Store` files.
- Use meaningful commit messages tied to the module or feature.

---

## 🧪 Testing Instructions

- Each module must include a test case in the `tests/` directory.
- Use `pytest` for testing.
- All tests should pass before progressing to the next module.

---

## 🔁 Execution Instructions

Wait for the user to issue the instruction:
> "✅ OK. Implement the next step."

## 🛠️ Development Workflow:
Then:
For each run, the LLM should:

1. Load all 3 files into memory (`idea.md`, `spec.md`, `prompt_plan.md`)
2. Find the **first module** in `prompt_plan.md` with `Status: Pending`
3. Read the corresponding spec and implement that module as a **Python file**
4. Return the full code block to the user
5. Once approved, update `prompt_plan.md` with `Status: Done`
