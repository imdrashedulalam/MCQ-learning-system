#!/bin/bash

# Create directories
mkdir -p pdf-mcq-exam-system/docs pdf-mcq-exam-system/database
cd pdf-mcq-exam-system

# ─── README.md ───
cat > README.md <<'EOF'
# PDF-Based MCQ Examination System

A full‑stack system that converts uploaded PDFs (question + correct answer pairs) into secure MCQ exams with automatic grading, re‑exam shuffling, and unlimited attempts.

## Features
- PDF parsing (digital + OCR for scanned)
- AI‑powered distractor generation (3 plausible wrong options)
- Secure exam environment (60‑min timer, no answer leakage)
- Auto‑grading with detailed review
- Question & option shuffling per attempt
- Unlimited attempts with score history
- Bengali option labels (`ক`, `খ`, `গ`, `ঘ`)

## Tech Stack
- **Frontend:** Next.js (React)
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **AI:** OpenAI / Local LLM
- **Deployment:** Docker, AWS

📖 Full documentation in [`/docs`](./docs/).
EOF

# ─── .gitignore ───
cat > .gitignore <<'EOF'
.env
__pycache__/
node_modules/
.next/
dist/
*.pyc
*.pdf
uploads/
EOF

# ─── DOCS ───
cat > docs/architecture.md <<'EOF'
# System Architecture

```mermaid
graph TD
    Client[Browser - React/Next.js]
    APIGateway[API Gateway / Load Balancer]
    Backend[FastAPI Server]
    DB[(PostgreSQL)]
    AI[AI Service (LLM/OCR)]
    Storage[(File Storage S3)]

    Client -->|HTTPS| APIGateway
    APIGateway --> Backend
    Backend --> DB
    Backend --> AI
    Backend --> Storage