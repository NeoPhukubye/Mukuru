# Money Coach API

A FastAPI backend for **Money Coach**, a financial companion for Mukuru remittance users.

## Features

- SQLite storage via SQLModel, with auto-seeded demo data for user **"grace"**.
- 8 endpoint groups: transactions, budget analysis, goals, simulate, advice, credit score, financial report (JSON + PDF), and coach chat.
- Rule-based, deterministic services (categorizer, advisor, credit engine, simulator, report generator).
- Optional LLM hook for coach chat behind an env var — falls back to rule-based replies so the demo works offline.
- CORS enabled for all origins.
- Unit tests for pure service functions (pytest).

## Run locally (one command)

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The server starts at `http://localhost:8000`. The OpenAPI docs are at `/docs`.

Demo user: `grace` (password not required — just pass `user_id=grace`).

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/transactions` | Add a single transaction |
| POST | `/transactions/bulk` | Add multiple transactions |
| GET | `/transactions` | List transactions (`user_id`, `category`, `from`, `to`) |
| GET | `/transactions/{id}` | Fetch one transaction (ownership-checked) |
| PATCH | `/transactions/{id}` | Partially update a transaction (ownership-checked) |
| DELETE | `/transactions/{id}` | Delete a transaction (ownership-checked) |
| GET | `/analyze-budget` | Monthly totals, savings rate, insights |
| POST | `/goals` | Create a savings goal |
| GET | `/goals` | List goals for a user |
| GET | `/goals/{id}/progress` | Goal progress with nudge string |
| PATCH | `/goals/{id}/add-funds` | Add money to a goal |
| DELETE | `/goals/{id}` | Delete a goal (ownership-checked) |
| POST | `/simulate` | Project balance and goal hit date |
| GET | `/advice` | Deterministic advisory engine |
| GET | `/calculate-credit-score` | Proprietary 300–850 score with breakdown |
| GET | `/generate-financial-report` | Structured JSON report |
| GET | `/generate-financial-report/pdf` | Downloadable PDF report |
| POST | `/coach/chat` | Intent-routed chat with optional LLM |
| GET | `/fx/currencies` | Supported currencies and live-rate availability |
| GET | `/fx/convert` | Convert an amount between currencies |

## Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | `sqlite:///./moneycoach.db` | Database connection |
| `GEMINI_API_KEY` | _(empty)_ | Enable Gemini-backed coach replies |
| `GEMINI_MODEL` | `gemini-3.5-flash` | Gemini model name |
| `GEMINI_TIMEOUT` | `20` | Gemini request timeout in seconds |
| `DEMO_USER_ID` | `grace` | Demo persona the seed data and reports target |
| `DEMO_USER_NAME` | `Grace` | Display name shown in the UI |
| `DEMO_ACCOUNT_HOLDER` | `Grace Moyo` | Name printed on the generated report |
| `DEMO_CURRENCY_SYMBOL` | `R` | Currency symbol used in coach prose |
| `CORS_ORIGINS` | `*` | Comma-separated allowed origins |
| `HOST` | `0.0.0.0` | Bind host |
| `PORT` | `8000` | Bind port |

The demo identity lives in `app/config.py`; the frontend reads the equivalent
values from `frontend/shared/api-config.js`, which every page loads. Override
either without editing code via `window.__MUKURU_USER__` /
`window.__MUKURU_API__` or the `mukuruUserId` / `mukuruApiBase` localStorage keys.

## Tests

```bash
cd backend
pytest -q
```

## Deploy

Deployed to Render at: **https://mukuru-jb1l.onrender.com**

The `render.yaml` config at the repo root handles the build, start command, env vars, and health check. CI runs on push via `.github/workflows/ci.yml`.

## Disclaimer

This product is for informational and educational purposes only and does not constitute financial advice.