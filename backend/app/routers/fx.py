"""Currency conversion endpoint."""
from __future__ import annotations

from fastapi import APIRouter, Query

from ..models import ErrorResponse, FxConversion, FxCurrencies
from ..services.fx import FX_COVERED, SUPPORTED_CURRENCIES, convert, currency_symbol

router = APIRouter(prefix="/fx", tags=["fx"])


@router.get("/currencies", response_model=FxCurrencies)
def fx_currencies() -> FxCurrencies:
    """List selectable currencies and whether a live rate is available."""
    return FxCurrencies(
        currencies=[
            {"code": code, "symbol": symbol, "fx_available": code in FX_COVERED}
            for code, symbol in SUPPORTED_CURRENCIES.items()
        ]
    )


@router.get("/convert", response_model=FxConversion, responses={422: {"model": ErrorResponse}})
def fx_convert(
    amount: float = Query(..., gt=0),
    from_currency: str = Query(..., min_length=3, max_length=3),
    to_currency: str = Query(..., min_length=3, max_length=3),
) -> FxConversion:
    """Convert an amount. Returns the original value when no rate exists."""
    converted, rate = convert(amount, from_currency, to_currency)
    return FxConversion(
        amount=amount,
        from_currency=from_currency.upper(),
        to_currency=to_currency.upper(),
        converted_amount=converted,
        rate=rate,
        symbol=currency_symbol(to_currency),
        converted=rate is not None,
    )