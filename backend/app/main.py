"""Money Coach — FastAPI application entrypoint."""
from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from . import seed as seed_module
from .db import create_db_and_tables
from .models import ErrorResponse
from .routers import advice, budget, coach, credit, goals, reports, simulate, transactions

app = FastAPI(
    title="Money Coach API",
    description="Financial companion for Mukuru remittance users.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _on_startup() -> None:
    create_db_and_tables()
    seed_module.seed()


@app.exception_handler(Exception)
async def _global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "internal_error", "detail": str(exc) or "Unexpected error."},
    )


app.include_router(transactions.router)
app.include_router(budget.router)
app.include_router(goals.router)
app.include_router(simulate.router)
app.include_router(credit.router)
app.include_router(reports.router)
app.include_router(coach.router)
app.include_router(advice.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}