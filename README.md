# AI Parallel Universe Decision Engine

[![Phase](https://img.shields.io/badge/Phase-1%20%E2%80%94%20Initial%20Working%20MVP-emerald)](#current-phase)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16%2B-black.svg)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0%2B-3178C6.svg)](https://www.typescriptlang.org/)

## Purpose

The **AI Parallel Universe Decision Engine** is a generalized AI-powered multi-agent decision intelligence system. It accepts hypothetical real-world scenarios written in natural language (e.g. *"India bans the sale of new petrol and diesel cars from 2035"*), dynamically detects affected domains, selects expert agents to perform independent evidence-backed analysis, synthesizes multi-domain findings, and projects plausible future outcomes across parallel universes (Optimistic, Baseline, Adverse) for decision-makers.

---

## Current Phase

**Phase 1 — Initial Working MVP**

*Phase 1 delivers the first end-to-end operational pipeline connecting the Next.js frontend with the FastAPI backend microservice engine. Users can enter any hypothetical decision scenario and receive structured multi-domain expert agent evaluations and parallel universe projections.*

---

## Pipeline Architecture

```text
User Natural-Language Scenario
             │
             ▼
   Scenario Understanding (Parser)
             │
             ▼
   Dynamic Domain Detection
             │
             ▼
    Dynamic Expert Selection
             │
             ▼
  Independent Expert Analysis (Multi-Agent)
             │
             ▼
     Multi-Domain Synthesis
             │
             ▼
  Parallel Universe Generation
             ├── 🟢 Optimistic Universe
             ├── 🔵 Baseline Universe
             └── 🔴 Adverse Universe
             │
             ▼
    Frontend Results Dashboard
```

---

## Supported Domains

The MVP dynamically evaluates and dispatches specialized expert agents across five supported domains:

1. **Automotive & Technology (`automotive`)**
   - *Focus:* Technology adoption, automotive manufacturing, vehicle platform transition, autonomous systems, software-defined vehicles, supply chain disruption.
2. **Energy (`energy`)**
   - *Focus:* Electricity demand, power generation, grid capacity, liquid fuel demand, renewable transition, battery storage, energy security.
3. **Environment (`environment`)**
   - *Focus:* Greenhouse gas emissions, air pollution, climate impact, resource consumption, battery recycling, ecological footprint.
4. **Economy (`economy`)**
   - *Focus:* Macroeconomic growth, capital allocation, consumer prices, government tax revenue, business margins, trade balances.
5. **Employment & Workforce (`employment`)**
   - *Focus:* Job creation, employment displacement, workforce retraining, skills transition, labor demand, vocational upskilling.

---

## API Endpoints

### 1. Health Check
- **`GET /api/health`**
- *Response:*
  ```json
  {
    "status": "ok",
    "service": "ai-parallel-universe-backend",
    "version": "0.1.0"
  }
  ```

### 2. Scenario Analysis
- **`POST /api/analyze`**
- *Request:*
  ```json
  {
    "scenario": "India bans the sale of new petrol and diesel cars from 2035."
  }
  ```
- *Response Structure:*
  ```json
  {
    "scenario": {
      "original_text": "India bans the sale of new petrol and diesel cars from 2035.",
      "scenario_type": "government_policy",
      "subject": "petrol and diesel vehicles",
      "action": "ban sales",
      "affected_entities": ["petrol vehicles", "diesel vehicles", "automotive manufacturers"],
      "location": { "country": "India" },
      "time": { "start_year": 2035 },
      "assumptions": ["Implementation proceeds as announced."],
      "uncertainties": []
    },
    "domains": [
      { "name": "automotive", "display_name": "Automotive & Technology", "relevance": 0.96, "reason": "..." },
      { "name": "energy", "display_name": "Energy", "relevance": 0.88, "reason": "..." }
    ],
    "experts": [
      { "name": "Automotive & Technology Expert", "domain": "automotive" },
      { "name": "Energy Expert", "domain": "energy" }
    ],
    "analyses": [ ... ],
    "synthesis": { ... },
    "parallel_universes": {
      "optimistic": { "title": "...", "summary": "...", "key_outcomes": [], "major_drivers": [], "risks": [] },
      "baseline": { "title": "...", "summary": "...", "key_outcomes": [], "major_drivers": [], "risks": [] },
      "adverse": { "title": "...", "summary": "...", "key_outcomes": [], "major_drivers": [], "risks": [] }
    }
  }
  ```

---

## Setup & Running the Project

### 1. Backend Setup

```bash
cd backend
python -m venv .venv

# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

# Start FastAPI server:
uvicorn app.main:app --reload --port 8000
```

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 2. Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local

# Start Next.js development server:
npm run dev
```

- **Web Application Dashboard:** [http://localhost:3000](http://localhost:3000)

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Default |
|---|---|---|
| `APP_ENV` | Application environment (`development`, `production`) | `development` |
| `LLM_API_KEY` | API Key for LLM provider (OpenAI compatible) | `""` |
| `LLM_MODEL` | LLM model identifier | `gpt-4o-mini` |
| `LLM_BASE_URL` | Base URL for LLM provider endpoint | `https://api.openai.com/v1` |
| `LLM_MOCK_MODE` | Enable deterministic dynamic fallback mode when API key is not present | `false` |
| `CORS_ORIGINS` | JSON list of allowed CORS origins | `["http://localhost:3000"]` |

### Frontend (`frontend/.env.local`)

| Variable | Description | Default |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | Base URL of backend FastAPI service | `http://localhost:8000` |

---

## Testing

Run automated tests using `pytest`:

```bash
cd backend
.venv\Scripts\python.exe -m pytest
```

---

## Verification Summary

- **Backend Unit & Pipeline Tests:** 7/7 tests passing.
- **Frontend Build:** Clean compilation with 0 TypeScript/Next.js errors.
- **End-to-End Flow:** Verified in live browser session (`http://localhost:3000` ➔ `POST /api/analyze` ➔ Multi-Agent Pipeline ➔ Dashboard Rendering).
