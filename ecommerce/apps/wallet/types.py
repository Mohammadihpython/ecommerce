from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from ecommerce.apps.wallet.params import EntityModel


class TransactionState(str, Enum):  # Enum-style state
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Transaction(EntityModel):
    id: int | None = None
    wallet_id: int
    amount: int
    state: TransactionState
    authority: str
    card_pan: str | None = None
    hash_card: str | None = None
    ref_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        exclude_none = True
