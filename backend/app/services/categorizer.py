"""Rule-based transaction categorizer. Pure functions, no I/O."""
from __future__ import annotations

import re

from ..models import Category, TransactionCreate

# Ordered patterns: first match wins.
# (keywords, category, is_remittance_rule)
_RULES: list[tuple[list[str], Category, bool]] = [
    (["remittance", "send money", "sendhome", "home remit", "mukuru send"], Category.REMITTANCE, True),
    (["rent", "rental", "lease", "municipal rates"], Category.RENT, False),
    (["grocery", "groceries", "checkers", "shoprite", "pick n pay", "spar", "supermarket", "food"], Category.GROCERIES, False),
    # "internet" is deliberately not in the airtime list. It appeared in both
    # this rule and the utilities one, and because airtime is checked first a
    # Telkom internet bill was filed as airtime.
    (["airtime", "data", "wifi", "prepaid", "cellphone", "mobile"], Category.AIRTIME, False),
    (["taxi", "uber", "bolt", "bus", "train", "transport", "fuel", "petrol", "diesel", "parking"], Category.TRANSPORT, False),
    (["electricity", "water", "municipal", "eskom", "telkom", "vodacom", "mtncell", "cell c", "internet", "broadband"], Category.UTILITIES, False),
]


def _matches(text: str, keywords: list[str]) -> bool:
    """Whole-word match, tolerating a simple plural "s".

    Plain substring matching was too loose: "Current account fee" matched
    "rent" inside "current", "Business loan" matched "bus", and "Spare parts"
    matched "spar".

    Only "s" is allowed, never "es". Allowing "es" would re-introduce the
    "spare parts" -> SPAR supermarket false positive.
    """
    return any(
        re.search(rf"\b{re.escape(keyword)}(?:s)?\b", text)
        for keyword in keywords
    )


def categorize(
    merchant: str,
    description: str,
    is_remittance: bool = False,
) -> Category:
    """Return the category for a transaction based on merchant/description."""
    text = f"{merchant} {description}".lower()

    if is_remittance:
        return Category.REMITTANCE

    for keywords, category, _ in _RULES:
        if _matches(text, keywords):
            return category

    return Category.OTHER


def build_transaction_category(tx: TransactionCreate) -> Category:
    """Categorize a TransactionCreate payload, honoring explicit category if valid."""
    if tx.is_remittance:
        return Category.REMITTANCE
    return categorize(tx.merchant, tx.description, tx.is_remittance)


def category_totals(transactions: list) -> dict[str, float]:
    """Aggregate amounts by category. Debits subtract, credits add."""
    totals: dict[str, float] = {}
    for tx in transactions:
        sign = 1.0 if tx.type == "credit" else -1.0
        cat = tx.category if isinstance(tx.category, str) else tx.category.value
        totals[cat] = totals.get(cat, 0.0) + sign * tx.amount
    return totals