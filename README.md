# Money Coach

> Turning a 1-minute remittance transaction into an everyday financial safety net.

Built for the **Mukuru Hackathon, Challenge B: Money Coach**.

Money Coach is a mobile-first financial companion for migrant workers who send money home. It tracks spending and remittances, helps users hit real goals (school fees, a fridge for home), coaches them in plain language, and turns their remittance history into a **credit score and formal financial document**, giving unbanked users a route into formal finance.

---

## The Problem

- Mukuru users interact in short, transactional bursts, which means low engagement and churn.
- Millions of migrant workers have no payslips or bank history, so they cannot access formal credit.
- Existing money tools are built for salaried, banked users and talk in jargon.

## The Solution

| Layer | What it does |
|-------|--------------|
| **Track** | Parses and categorizes transactions (groceries, rent, airtime, remittances) |
| **Plan** | Goal tracking, "what if I save R100 a week" simulator, advisory engine |
| **Coach** | Conversational AI coach with proactive smart nudges |
| **Prove** | Remittance-based credit score and downloadable formal financial document |

### Meet Grace

Grace works in Johannesburg and sends money home every payday. She is saving for school fees and a fridge. Money Coach nudges her when she is R150 from her goal, builds her credit score from her consistent remittances, and generates a formal statement she can take to a lender.

---

## Features

**Core**
- Expense and remittance tracking with automatic categorization
- Goal-setting with real-time progress
- Plain-language guidance, available in **7 languages** (English, isiZulu, Sesotho, chiShona, Chichewa, French, Portuguese)

**Advisory and Planning**
- Financial planner: monthly injection amount and pool allocation (emergency, goals, investment)
- Savings simulator with projected milestones
- AI chat coach with smart nudges

**Bonus**
- Remittance-based credit score (300 to 850) with per-factor breakdown and history
- Formal financial document (JSON and PDF)

---

## Architecture

```
┌──────────────────────┐        REST/JSON        ┌───────────────────────────┐
│      Frontend        │ ──────────────────────▶ │     FastAPI Backend       │
│ Dashboard | Chat |   │ ◀────────────────────── │ routers → services → DB   │
│ Onboarding | Reports │                         │                           │
└──────────────────────┘                         │ categorizer  advisor      │
                                                 │ simulator    credit_engine│
                                                 │ report_generator  coach   │
                                                 └─────────────┬─────────────┘
                                                               │
                                                        SQLite (seeded)
```

Separation of concerns: the frontend only consumes the API contract, and all financial logic lives in pure, tested service functions on the backend.

### Repository Structure

```
Mukuru/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, CORS, router wiring, /health
│   │   ├── models.py            # Pydantic contracts + SQLModel tables
│   │   ├── db.py                # Engine, session, query helpers
│   │   ├── seed.py              # Demo data for user "grace"
│   │   ├── routers/             # transactions, budget, goals, simulate,
│   │   │                        # advice, credit, reports, coach
│   │   └── services/            # categorizer, advisor, simulator,
│   │                            # credit_engine, report_generator, coach
│   ├── tests/test_services.py
│   ├── conftest.py
│   ├── requirements.txt
│   └── README.md                # Backend-specific reference
├── frontend/
│   ├── Dashboard/               # Auth + main dashboard
│   ├── ai-chat/                 # Money Coach chat (calls the API)
│   └── Reports and polish/      # Onboarding, account, report pages
├── .github/workflows/ci.yml     # test → smoke test
├── render.yaml                  # Render blueprint
└── README.md
```

---

## Tech Stack

- **Backend:** Python 3.11, FastAPI, SQLModel/SQLite, Pydantic v2, ReportLab, pytest
- **Frontend:** Vanilla HTML / CSS / JavaScript — **no build step, no npm**. Static files served directly, so the app loads on low-bandwidth connections.
- **AI coach:** Rule-based intent routing with an optional Gemini hook (env-gated), offline-safe fallback

---

## Getting Started

### Prerequisites
- Python 3.11+
- A web browser (any static file server works)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- Demo data for **Grace** (`user_id=grace`) is seeded automatically on startup.

### Frontend

The frontend has no dependencies to install — just serve the folder:

```bash
cd frontend
python3 -m http.server 8001
```

Then open http://localhost:8001/Dashboard/index.html

The chat app currently targets the deployed API (`https://mukuru-jb1l.onrender.com`); the URL is set at the top of `frontend/ai-chat/script.js` and can be repointed at a local backend.

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `DATABASE_URL` | SQLite connection string | `sqlite:///./moneycoach.db` |
| `GEMINI_API_KEY` | Optional: enables Gemini-powered coach replies | _unset (rule-based fallback)_ |
| `GEMINI_MODEL` | Gemini model name | `gemini-2.0-flash` |
| `GEMINI_TIMEOUT` | Gemini request timeout (seconds) | `10` |
| `HOST` / `PORT` | Server bind address | `0.0.0.0` / `8000` |

### Tests

```bash
cd backend
pytest -q
```

The suite covers the pure service functions (categoriser, credit engine, simulator, advisor, report generator), the API contracts (period scoping, credit-score agreement between endpoints, goal and transaction ownership isolation), and the transaction CRUD endpoints. `ruff check .` runs in CI alongside the tests.

---

## CI/CD & Deployment

`.github/workflows/ci.yml` runs on every push and pull request:

1. Install dependencies (Python 3.11)
2. Run `pytest -q`
3. Smoke-test the server by booting uvicorn on `127.0.0.1` and hitting `/health` and `/analyze-budget?user_id=grace`

**Deployment is handled by Render directly**, not by CI. `render.yaml` sets `autoDeploy: true`, so pushing to `main` triggers a build and deploy without any GitHub Actions step or API keys.

Live at **https://mukuru-jb1l.onrender.com** — `/` redirects to `/docs`, and `/health` returns `{"status": "ok"}`.

To re-apply the blueprint manually:

```bash
render deploy --dir . --yaml render.yaml
```

Notes:
- The root `requirements.txt` is a one-line shim delegating to `backend/requirements.txt`.
- The SQLite file lives on the service's ephemeral disk, so **data resets on each deploy** — fine for a demo, but a persistent disk or hosted database is needed for real use.
- Set `GEMINI_API_KEY` in the Render dashboard to activate LLM coach replies.

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Redirects to `/docs` |
| GET | `/health` | Liveness probe (used by Render) |
| POST | `/transactions` | Add a single transaction |
| POST | `/transactions/bulk` | Add up to 200 transactions at once |
| GET | `/transactions` | List transactions (`user_id`, `category`, `from`, `to`) |
| GET | `/transactions/{id}` | Fetch one transaction (ownership-checked) |
| PATCH | `/transactions/{id}` | Partially update a transaction (ownership-checked) |
| DELETE | `/transactions/{id}` | Delete a transaction (ownership-checked) |
| GET | `/analyze-budget` | Category totals, savings rate, plain-language insights |
| POST | `/goals` | Create a savings goal |
| GET | `/goals` | List a user's goals |
| GET | `/goals/{id}/progress` | Percent complete, remaining amount, nudge |
| PATCH | `/goals/{id}/add-funds` | Add money to a goal |
| DELETE | `/goals/{id}` | Delete a goal (ownership-checked) |
| POST | `/simulate` | "What if I save R__ a week" projection |
| GET | `/advice` | Monthly injection and pool allocation |
| GET | `/calculate-credit-score` | Score, band, factor breakdown, history, tips |
| GET | `/generate-financial-report` | Structured financial report (JSON) |
| GET | `/generate-financial-report/pdf` | Downloadable formal statement |
| POST | `/coach/chat` | Chat with the Money Coach |
| GET | `/fx/currencies` | Supported currencies and live-rate availability |
| GET | `/fx/convert` | Convert an amount between currencies |

Full request/response schemas are available at `/docs`.

### Errors

Domain errors return a consistent shape:

```json
{ "error": "no_data", "detail": "No transactions found for this user." }
```

`no_data` (HTTP 400) is returned when an analysis endpoint is called for a user with no transactions, and `not_found` (HTTP 404) when a goal does not exist or does not belong to the caller. Schema validation failures return FastAPI's standard HTTP 422 response.

---

## Credit Score Methodology

Score range **300 to 850**, built from remittance behavior rather than bank history:

| Factor | Weight | What it measures |
|--------|--------|------------------|
| Consistency | 0.35 | Share of months containing a remittance |
| Stability | 0.15 | Coefficient of variation of remittance amounts |
| Timing | 0.15 | Share of remittances sent by the 25th |
| Tenure | 0.10 | Length of transaction history (capped at 24 months) |
| Savings behavior | 0.25 | Surplus retained as a share of income |

The breakdown and weights are returned with every score so users see exactly how to improve it. Bands: **Excellent** ≥ 750, **Very Good** ≥ 650, **Good** ≥ 550, **Fair** ≥ 450, else **Poor**.

> This is a prototype scoring model for demonstration. It is not a regulated credit bureau score.

---

## Demo Flow

1. Grace opens the dashboard and sees spending by category and goal progress.
2. She sends money home on payday, and the transaction is categorized automatically.
3. A smart nudge appears: "You're R150 away from your school-fee goal!"
4. She runs the simulator: "What if I save R100 a week?"
5. Her credit score ticks upward on the score tracker.
6. She generates and downloads her formal financial statement.

---

## Judging Criteria Alignment

| Criterion | How we address it |
|-----------|-------------------|
| **Functionality** | End-to-end flow: track, plan, coach, score, document — 13 live endpoints |
| **Creativity and UX** | Remittance-backed credit for the unbanked; chat-first, mobile-first, low-bandwidth design |
| **Technical Implementation** | Clean API contract, tested pure services, deterministic engines, offline-safe AI |
| **Presentation** | Story-led demo around Grace, with a clear business case for Mukuru retention |

---

## Team

| Role | Responsibility | Member |
|------|----------------|--------|
| Backend | API, advisory engine, credit engine, report generator | _name_ |
| Frontend Lead 1 | Dashboard, charts, goal progress | _name_ |
| Frontend Lead 2 | AI chat, nudges, simulator UI | _name_ |
| Frontend Lead 3 | Onboarding, reports, branding and polish | _name_ |
| Business Lead | Lean canvas, pitch deck, demo narrative | _name_ |

---

## Roadmap

- Wire the dashboard and report pages to the live API (currently demo data)
- Live Mukuru transaction feed integration
- Multilingual *coach replies* (the UI is already translated; the coach's answers are English-only)
- USSD/WhatsApp channel for low-bandwidth access
- Partnerships with lenders to accept the formal statement
- Regulated, bureau-grade scoring model

---

## Disclaimer

Hackathon prototype. Demo data is synthetic. Credit scores and advice are illustrative and not financial advice.
