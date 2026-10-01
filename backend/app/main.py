"""Money Coach — FastAPI application entrypoint."""
from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from . import seed as seed_module
from .db import create_db_and_tables
from .models import ErrorResponse
from .routers import advice, budget, coach, credit, fx, goals, reports, simulate, transactions

logger = logging.getLogger("moneycoach")

# Browsers reject a wildcard origin when credentials are allowed, so the
# wildcard is only valid with credentials off.
ALLOW_ORIGINS = [
    o.strip()
    for o in os.environ.get("CORS_ORIGINS", "*").split(",")
    if o.strip()
]

_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    422: "validation_error",
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_module.seed()
    yield


app = FastAPI(
    title="Money Coach API",
    description="Financial companion for Mukuru remittance users.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials="*" not in ALLOW_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def _http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Flatten the error envelope to {"error": ..., "detail": ...}.

    Routers raise HTTPException with a dict detail, which Starlette otherwise
    nests under "detail", producing {"detail": {"error": ...}} and breaking
    the documented response shape.
    """
    detail = exc.detail
    if isinstance(detail, dict):
        content = detail
    else:
        content = {"error": _ERROR_CODES.get(exc.status_code, "error"), "detail": str(detail)}
    return JSONResponse(status_code=exc.status_code, content=content)


@app.exception_handler(Exception)
async def _global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # Log the detail server-side; never return raw exception text, which can
    # leak SQL, file paths, or configuration to callers.
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "internal_error", "detail": "An unexpected error occurred."},
    )


app.include_router(transactions.router)
app.include_router(budget.router)
app.include_router(goals.router)
app.include_router(simulate.router)
app.include_router(credit.router)
app.include_router(reports.router)
app.include_router(coach.router)
app.include_router(advice.router)
app.include_router(fx.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")