# Project 5 — Agentic Workflow

This repository contains a small **agentic AI system** created for the Udacity Agentic AI project. The implementation is a **Responsible Academic Planning Agent** that supports students with study planning, concept review, and safe redirection when a request would violate academic integrity.

---

## 📌 Project Overview

The system is a **single-agent workflow** designed to demonstrate:
- **reasoning and decision logic** for different student requests,
- **limited memory/state handling** using a bounded short-term memory buffer,
- **tool use** through local helper functions for policy checks, resource lookup, and schedule building,
- **safeguards** for transparency, reliability, and responsible use.

The agent is intentionally scoped for **academic support only**. It does **not** complete graded submissions for the user.

---

## 🧠 Agent Workflow

The agent follows this sequence:
1. Accept a user request.
2. Classify the request intent and risk level.
3. Detect the topic and any time constraints.
4. Select the appropriate tool(s):
   - `policy_lookup`
   - `resource_lookup`
   - `schedule_builder`
5. Generate a transparent response.
6. Store a short memory entry for recent interactions.

---

## 📁 Repository Contents

- `agentic_system.ipynb` — notebook version with explanations, code, architecture notes, and example runs
- `agentic_system.py` — script version of the agentic workflow
- `Agentic_AI_System_Design_Report.md` — written design and ethics analysis report
- `Agentic_AI_System_Design_Report.pdf` — PDF export of the final report
- `architecture_diagram.mmd` — Mermaid source for the architecture diagram
- `agent_outcomes.png` — chart generated from representative test runs
- `requirements.txt` — reproducibility file created from the active Python environment

---

## ⚙️ Setup Instructions

### 1. Activate the virtual environment
```bash
source .venv/bin/activate
```

### 2. Install dependencies if needed
```bash
pip install -r requirements.txt
```

### 3. Run the script
```bash
python agentic_system.py
```

### 4. Run the notebook
Open `agentic_system.ipynb` in VS Code or Jupyter and execute the cells from top to bottom.

---

## ✅ Expected Behavior

The agent was tested on representative prompts and showed the following behavior:
- generated study plans for legitimate learning requests,
- recommended topic-specific resources,
- tracked recent interactions in short-term memory,
- refused integrity-risk prompts such as requests to complete graded work.

The output chart in `agent_outcomes.png` summarizes the supported vs. redirected outcomes from the evaluation examples.

---

## 🔒 Safety and Transparency Features

This project includes basic safeguards:
- keyword-based detection of academic-integrity risk,
- refusal and redirection for unsafe requests,
- visible reporting of intent, risk, tools used, and final status,
- bounded memory to reduce uncontrolled context growth.

---

## ⚠️ Limitations

This is an educational prototype, not a production application. Current limitations include:
- rule-based classification rather than a robust learned model,
- a small local resource database,
- limited personalization,
- evaluation on a small number of representative prompts.

---

## 📚 Deliverables Summary

This submission includes all required project artifacts:
- agent notebook/script,
- design report with citations,
- architecture documentation,
- reproducibility file via `pip freeze > requirements.txt`.

---

## Author Note

This project was built for academic demonstration of **agentic workflow design**, **tool orchestration**, **memory handling**, and **responsible AI behavior**.