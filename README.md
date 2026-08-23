# AI Tester Blueprint 4X

A chapter-based, hands-on framework for building an AI-powered QA toolchain — from prompt engineering and LLM safety rules to local test case generation, job-hunt automation, and personal branding.

> **Work in Progress** — This README reflects the framework as of today. New chapters and tools will be added over time; treat this document as a living snapshot, not the final version.

## The Journey (Chapter by Chapter)

| # | Chapter | What It Covers |
|---|---------|----------------|
| 1 | **LLM Basics** | Ground rules for evidence-based AI QA work — no fabrication, no assumptions, mandatory traceability, and confidence labeling |
| 2 | **Prompt Engineering** | The RICE POT structured prompt template, a planned Salesforce Selenium framework, and a 54-skill QA prompt suite |
| 3 | **Local Test Case Generator** | A Streamlit app that turns a Jira ticket into test cases using a local LLM with a cloud fallback |
| 4 | **JobKitAI** | A resume-tailoring skill that matches your resume to a job description and produces ATS-safe, editable output |
| 5 | **JobTrackerAI** | A local-first Kanban board for tracking job applications (React + Vite + IndexedDB) |
| 6 | **Branding & LinkedIn Skills** | LinkedIn branding and skills material |

## Chapter Details

### Chapter 1 — LLM Basics
- `Anti-Hallucination.rules.md` — a strict rulebook for AI acting as a QA assistant: only use provided evidence (PRD, user stories, API docs, logs), never invent features or behaviors, mark untraceable claims, and always separate *Verified Facts* from *Assumptions* and *Missing Information*.

### Chapter 2 — Prompt Engineering
- `RICE_POT_Template.md` — the seven-part prompt framework: **R**ole, **I**nstructions, **C**ontext, **E**xpected, **P**arameters, **O**utput, **T**ask.
- `04_Plan_Framework.md` — decoded example: a Salesforce login automation framework plan (Selenium + Java + Maven + TestNG, PageFactory, xpath-only locators, no `Thread.sleep`).
- `RICE_POT_SeleniumAdvance/` — the Maven/TestNG Selenium project scaffold built from that plan.
- `prompt_templates/` — 54 installable QA skills (STLC phases, Playwright, Selenium, API testing, AI safety/guardrails, test deliverables).

### Chapter 3 — Local Test Case Generator
A two-screen Streamlit app (`src/`):
- **Chat screen** — type "create test cases for JIRA-102"; the app fetches the ticket via the Jira REST API, merges it into `templates/testcase_creator.md`, and generates test cases.
- **Settings screen** — persist Jira URL/email/token and LLM provider credentials.
- **LLM backend** — local Ollama (`gemma3:1b`) first, with automatic fallback to Groq (`llama-3.1-8b-instant`). Credentials live in `.env` / `config.json`, never in code.

### Chapter 4 — JobKitAI
- `resume-helper/resume-tailor/` — a `resume-tailor` skill that cross-references your resume against a job description, tailors honest, keyword-matched bullets, and gates on a human review step.
- `Job_description_22_Aug_2026/` — LinkedIn job descriptions (CSV) used as tailoring input.
- `output/` — tailored, deliverable `.docx` resumes.

### Chapter 5 — JobTrackerAI
A private, local-first Kanban board for job applications:
- React 18 + Vite + Tailwind CSS
- Drag-and-drop pipelines via `@dnd-kit` (Wishlist → Applied → Follow-up → Interview → Offer → Rejected)
- IndexedDB storage via `idb` — all data stays in the browser, no server

### Chapter 6 — Branding & LinkedIn Skills
- `files.zip` — LinkedIn branding and skills resources.

## Tech Stack Overview

| Area | Technology |
|------|------------|
| AI prompts & rules | RICE POT template, anti-hallucination rulebook |
| Local LLM | Ollama (`gemma3:1b`) |
| Cloud fallback | Groq API |
| Automation framework | Selenium + Java + Maven + TestNG (Page Object Model) |
| Test case generator | Python + Streamlit + Jira REST API |
| Job tracker | React + Vite + Tailwind + IndexedDB |

## Getting Started

This is a learning framework — each chapter is self-contained. Pick your starting point:

```bash
# Chapter 3: Jira Test Case Generator
cd chapter_03_Local_TC_Generator
pip install -r src/requirements.txt
streamlit run src/app.py

# Chapter 5: Job Tracker
cd chapter_05_JobTrackerAI
npm install
npm run dev

# Chapter 2: Selenium Framework (requires Java + Maven)
cd Chapter_2_Prompt_eng/RICE_POT_SeleniumAdvance
mvn test
```

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.

## Author

Md Twasif Hossain

## License

MIT
