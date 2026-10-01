"""Rule-based transaction categorizer. Pure functions, no I/O."""
from __future__ import annotations

from ..models import Category, TransactionCreate

# Ordered patterns: first match wins.
_RULES: list[tuple[list[str], Category, bool]] = [
    (["remittance", "send money", "sendhome", "home remit", "mukuru send"], Category.REMITTANCE, True),
    (["rent", "lease", "municipal rates"], Category.RENT, False),
    (["grocer", "grocery", "checkers", "shoprite", "pick n pay", "pick n pay", "spar", "supermarket", "food"], Category.GROCERIES, False),
    (["airtime", "data", "internet", "wifi", "prepaid", "cellphone", "mobile"], Category.AIRTIME, False),
    (["taxi", "uber", "bolt", "bus", "train", "transport", "fuel", "petrol", "diesel", "parking"], Category.TRANSPORT, False),
    (["electricity", "water", "municipal", "eskom", "telkom", "vodacom", "mtncell", "cell c", "internet", "broadband"], Category.UTILITIES, False),
]


def _matches(text: str, keywords: list[str]) -> bool:
    return any(k in text for k in keywords)


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