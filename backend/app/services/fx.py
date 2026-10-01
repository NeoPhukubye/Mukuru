"""Currency conversion via the Frankfurter API.

Frankfurter (https://frankfurter.dev) serves ECB reference rates over HTTPS,
requires no API key, and is MIT licensed. The api.frankfurter.app host now
301-redirects here, so the v1 path is used directly. Keeping the call in one
place means the rest of the app stays offline-safe: a network failure
degrades to the original amount rather than raising.
"""
from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger("moneycoach.fx")

FRANKFURTER_BASE = "https://api.frankfurter.dev/v1/latest"

# Symbols the dashboard offers in its currency selector.
SUPPORTED_CURRENCIES = {
    "ZAR": "R",
    "USD": "$",
    "MWK": "MK",
    "ZMW": "K",
    "KES": "KSh",
    "GBP": "£",
    "EUR": "€",
}

# Frankfurter publishes ECB reference rates for 30 currencies. The African
# corridors Mukuru serves most (ZMW, MWK, KES) are not among them, so those
# conversions are unavailable and callers get the original amount back.
FX_COVERED = frozenset({
    "AUD", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD",
    "HUF", "IDR", "ILS", "INR", "ISK", "JPY", "KRW", "MXN", "MYR", "NOK",
    "NZD", "PHP", "PLN", "RON", "SEK", "SGD", "THB", "TRY", "USD", "ZAR",
})


def currency_symbol(code: str) -> str:
    return SUPPORTED_CURRENCIES.get(code.upper(), code.upper())


def _fetch_rate(from_currency: str, to_currency: str) -> Optional[float]:
    import httpx

    try:
        resp = httpx.get(
            FRANKFURTER_BASE,
            params={"from": from_currency, "to": to_currency},
            timeout=5.0,
        )
        resp.raise_for_status()
        return float(resp.json()["rates"][to_currency])
    except Exception as exc:  # network, malformed payload, unknown pair
        logger.warning("FX lookup failed for %s->%s: %s", from_currency, to_currency, exc)
        return None


def convert(amount: float, from_currency: str, to_currency: str) -> tuple[float, Optional[float]]:
    """Convert `amount`, returning (converted_amount, rate_used).

    On failure returns the original amount and rate None, so callers can show
    an unconverted figure rather than an error.
    """
    src = from_currency.upper()
    dst = to_currency.upper()
    if src == dst:
        return round(amount, 2), 1.0
    if dst not in FX_COVERED:
        # No published rate for this pair. Skip the network call entirely.
        logger.info("No Frankfurter rate for %s->%s; leaving amount unchanged", src, dst)
        return round(amount, 2), None

    rate = _fetch_rate(src, dst)
    if rate is None:
        return round(amount, 2), None
    return round(amount * rate, 2), rate


def supported() -> dict[str, str]:
    return dict(SUPPORTED_CURRENCIES)