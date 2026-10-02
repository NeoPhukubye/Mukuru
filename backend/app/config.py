"""Runtime configuration, read once from the environment.

Demo identity and display defaults used to be literals scattered across
seed.py and routers/reports.py, so changing the persona meant finding every
copy. They live here now; each is overridable per environment.
"""
from __future__ import annotations

import os

# The demo persona. Authentication is mocked, so this is not a credential -
# it only selects which seeded dataset the frontend and reports display.
DEMO_USER_ID = os.environ.get("DEMO_USER_ID", "grace")
DEMO_USER_NAME = os.environ.get("DEMO_USER_NAME", "Grace")
DEMO_ACCOUNT_HOLDER = os.environ.get("DEMO_ACCOUNT_HOLDER", "Grace Moyo")

# Currency symbol used in coach replies and report text. The dashboard has its
# own selector, but the backend previously hardcoded "R" in prose regardless.
DEMO_CURRENCY_SYMBOL = os.environ.get("DEMO_CURRENCY_SYMBOL", "R")


def account_holder_for(user_id: str) -> str:
    """Display name for a user, falling back to a readable form of the id."""
    if user_id == DEMO_USER_ID:
        return DEMO_ACCOUNT_HOLDER
    return user_id.replace("_", " ").replace("-", " ").title()