

from typing import Optional
from pydantic import BaseModel,ConfigDict
from datetime import datetime
from ecommerce.apps.wallet.types import TransactionState


class EntityModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        populate_by_name=True,
        str_strip_whitespace=True,
        json_encoders={BaseModel: lambda m: m.model_dump(exclude_unset=True)},
    )

    def dict(self, *args, **kwargs):
        kwargs.setdefault("exclude_unset", True)
        return super().model_dump(*args, **kwargs)

    def json(self, *args, **kwargs):
        kwargs.setdefault("exclude_unset", True)
        return super().model_dump_json(*args, **kwargs)
class CreateWalletRequest(EntityModel):
    user_id: int


class CreateWalletResponse(EntityModel):
    user_id: int
    wallet_id : int

class PaymentRequest(EntityModel):
    user_id:int
    amount: int
    IPG: str
# internal payment gateway == ipg
class CreatePaymentRequest(EntityModel):
    wallet_id : int
    amount: int
    ipg : str

class CreatePaymentResponse(EntityModel):
    wallet_id : int
    amount: int
    payment_url: str
    authority: str

class CallbackRequest(EntityModel):
    ipg_key: str
    authority: str
    status:str


class CallbackResponse(BaseModel):
    amount: Optional[int]=None
    state: TransactionState
    ref_id: Optional[int]=None
    card_pan: Optional[str]=None
    hash_card: Optional[str]=None
    processed_at: Optional[datetime]=None

    class Config:
        exclude_none = True


class VerifyRequest(BaseModel):
    ipg: str
    amount: int
    authority: str