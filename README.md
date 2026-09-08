# AI Parallel Universe Decision Engine

[![Phase](https://img.shields.io/badge/Phase-0%20%E2%80%94%20Project%20Foundation-blue)](#current-phase)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15%2B-black.svg)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0%2B-3178C6.svg)](https://www.typescriptlang.org/)

## Purpose

The **AI Parallel Universe Decision Engine** is a generalized AI-powered multi-agent decision intelligence system. It accepts hypothetical real-world scenarios written in natural language (e.g. *"India bans the sale of new petrol and diesel cars from 2035"*), dynamically detects affected domains, selects expert agents to perform independent evidence-backed analysis, synthesizes consensus and conflicts, models temporal/causal flows, and generates plausible future scenarios for decision-makers.

---

## Current Phase

**Phase 0 — Project Foundation & Development Setup**

*Phase 0 establishes the core repository structure, FastAPI backend service, Next.js frontend web interface, environment configuration, health monitoring endpoints, and test suite. The AI reasoning pipeline and agents will be implemented in subsequent phases.*

---

## Target Architecture

```text
               User Scenario Input
                        ↓
             Scenario Understanding
                        ↓
            Dynamic Domain Detection
                        ↓
            Dynamic Expert Selection
                        ↓
        Independent Multi-Agent Analysis
                        ↓
           Evidence Retrieval / RAG
                        ↓
        Conflict & Consistency Analysis
                        ↓
             Consensus / Synthesis
                        ↓
          Future Scenario Generation
                        ↓
          Temporal & Causal Analysis
                        ↓
            Decision Intelligence
                        ↓
                 Interactive Dashboard
```

---

## Repository Structure

```text
AI-Parallel-Universe/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app initialization, middleware, lifecycle
│   │   ├── config.py        # Pydantic Settings environment configuration
│   │   ├── api/             # API Router & route handlers
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── schemas/         # Strongly typed Pydantic data models
│   │   │   ├── __init__.py
│   │   │   └── health.py
│   │   ├── services/        # Business logic placeholders
│   │   ├── agents/          # Multi-agent logic placeholders
│   │   ├── graph/           # Workflow orchestration placeholders
│   │   ├── evidence/        # Evidence retrieval & RAG placeholders
│   │   └── analysis/        # Conflict & temporal analysis placeholders
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_health.py   # Health check automated unit test
│   ├── requirements.txt
│   └── .env.example
├── frontend/                # Next.js TypeScript web application
│   ├── app/
│   │   ├── layout.tsx
│   │   └── page.tsx         # Backend connection status interface
│   ├── lib/
│   │   └── api.ts           # API service abstraction
│   ├── .env.example
│   └── package.json
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── .gitignore
└── README.md
```

---

## Backend Setup

### Prerequisites
- Python 3.11+ (or Python 3.10+)

### Setup Instructions

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   - On Linux/macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - On Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

5. **Start the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

6. **Verify API Endpoints:**
   - **Health API:** [http://localhost:8000/api/health](http://localhost:8000/api/health)
   - **Swagger Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **ReDoc Documentation:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Frontend Setup

### Prerequisites
- Node.js v18.17+ / v20+ / v22+
- npm v9+

### Setup Instructions

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment variables:**
   Copy `.env.example` to `.env.local`:
   ```bash
   cp .env.example .env.local
   ```
   Ensure `NEXT_PUBLIC_API_URL` points to your backend (`http://localhost:8000`).

4. **Start the development server:**
   ```bash
   npm run dev
   ```

5. **Open Application:**
   Access the dashboard at [http://localhost:3000](http://localhost:3000).

---

## Testing

Run automated backend tests using `pytest`:

```bash
cd backend
pytest
```

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Default |
|---|---|---|
| `APP_ENV` | Application environment (`development`, `production`) | `development` |
| `OPENAI_API_KEY` | API Key for LLM provider (optional in Phase 0) | `""` |
| `DATABASE_URL` | Database connection string (optional in Phase 0) | `""` |
| `CORS_ORIGINS` | JSON list of allowed CORS origins | `["http://localhost:3000"]` |

### Frontend (`frontend/.env.local`)

| Variable | Description | Default |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | Base URL of backend FastAPI service | `http://localhost:8000` |
