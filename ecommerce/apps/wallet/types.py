
from enum import Enum
from datetime import datetime
from typing import Optional
from uuid import UUID

from ecommerce.apps.wallet.params import EntityModel

class TransactionState(str,Enum):  # Enum-style state
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"



class Transaction(EntityModel):
    id: Optional[int] = None
    wallet_id: int
    amount: int
    state: TransactionState
    authority: str
    card_pan: Optional[str]=None
    hash_card: Optional[str]=None
    ref_id: Optional[int]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None

    class Config:
        exclude_none = True