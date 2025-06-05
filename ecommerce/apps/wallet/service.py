
from datetime import datetime
from typing import Protocol,Callable,Any


from ecommerce.apps.wallet.params import(
CallbackRequest,
CallbackResponse,
CreatePaymentRequest,
CreatePaymentResponse,
VerifyRequest,
PaymentRequest,


)
from ecommerce.apps.wallet.types import Transaction, TransactionState



class Repository(Protocol):
    def create_wallet(self,user_id: int,) -> int:
        """Create a wallet for the user with the given user_id."""
        ...

    def get_wallet_by_user_id(self, user_id: int) -> int:
        """Retrieve the wallet for the user with the given user_id."""
        ...
    def upsert_transaction(self,transaction: Transaction)-> Transaction:
        """Insert or update a transaction in the database."""
        ...
    def update_balance(self,wallet_id: int, amount: int) -> int:
        """Update the balance of the wallet with the given wallet_id."""
        ...
    def get_wallet_balance(self,wallet_id: int) -> int:
        """Retrieve the balance of the wallet with the given wallet_id."""
        ...
    def get_transaction_by_authority(self,authority: str) -> Transaction:
        ...

    def transaction_lock(self,wallet_id:int,fun: Callable[[],Any])-> CallbackResponse:
        """Lock the transaction for the given wallet_id and execute the function."""
        ...

    def review_transaction(self) -> None:
        """Review a transaction and update its state. and cancel the transaction of 12 hour pass that
        its state is pending.
        """
        ...



class IPG(Protocol):
    def create_payment_request(
        self,
        create_payment_request:CreatePaymentRequest
    ) -> CreatePaymentResponse:
        """Create a payment request and return the authority."""
        ...

    def availableIPGs(self)-> list[str]:
        """Return a list of available IPGs."""
        ...
    def verify_payment(self,vReq:VerifyRequest)-> CallbackResponse:
        """Verify the payment and return the callback response."""
        ...


class PaymentService:
    def __init__(self, repository: Repository, ipg: IPG):
        self.repo = repository
        self.paymentGateway = ipg


    def IPGList(self)->list[str]:
        """Return a list of available IPGs."""
        return self.paymentGateway.availableIPGs()



    def initialPaymentRequest(self,req :PaymentRequest)->CreatePaymentResponse:
        """Create a payment request and return the authority."""
        # Check if the IPG is available
        availableIPGs = self.paymentGateway.availableIPGs()
        if req.IPG not in self.paymentGateway.availableIPGs():
            raise ValueError(f"IPG {req.IPG} is not available.")

        # Get the wallet ID for the user
        try:
          wallet_id = self.repo.get_wallet_by_user_id(req.user_id)

        except Exception as e:
            raise RuntimeError(f"Unexpected error fetching wallet: {e}")


        create_payment_request = CreatePaymentRequest(
            wallet_id=wallet_id,
            amount=req.amount,
            ipg=req.IPG
        )
        try:
            paymentResp=self.paymentGateway.create_payment_request(create_payment_request)
        except Exception as e:
            raise RuntimeError(f"Error creating payment request: {e}")

        transaction = Transaction(
            wallet_id=paymentResp.wallet_id,
            amount=paymentResp.amount,
            state= TransactionState.PENDING,
            authority=paymentResp.authority,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        try:
            self.repo.upsert_transaction(transaction)
        except Exception as e:
            raise RuntimeError(e)

        return paymentResp

    def callBackHandler(self,req:CallbackRequest)->CallbackResponse:

        # get old transaction
        try:
            oldTran= self.repo.get_transaction_by_authority(req.authority)
        except Exception as e:
            raise RuntimeError(f"Error Get transaction:{e}")

        if oldTran.state in [TransactionState.SUCCESS, TransactionState.FAILED]:
            return CallbackResponse(
                state=oldTran.state,
                processed_at=oldTran.updated_at
            )

        # Handle failed status
        if req.status != "OK":
            return self.handleFailedStatus(oldTran,req.authority)

        try:
           verify_request = self.verifyRequest(oldTran,req.authority)
        except Exception as e:
            raise RuntimeError(f"Error verifying request: {e}")
        # Handle success status
        return self.repo.transaction_lock(oldTran.wallet_id, lambda: self.process_payment(oldTran, verify_request))




    def handleFailedStatus(self,t:Transaction,authority:str)-> CallbackResponse:
        failedTran =t.model_copy(update={
            "state": TransactionState.FAILED,
            "updated_at":datetime.now(),
        })

        try:
            fTran = self.repo.upsert_transaction(failedTran)
        except Exception as e:
            raise RuntimeError("failed to update transaction :{e}")
        return CallbackResponse(
            state= fTran.state,
            processed_at=fTran.updated_at
        )

    def verifyRequest(self,t:Transaction,ipgKey:str) -> CallbackResponse:
        verify_request = VerifyRequest(
            authority=t.authority,
            amount=t.amount,
            ipg=ipgKey,
        )
        try:
            v_resp = self.paymentGateway.verify_payment(verify_request)
        except Exception as e:
            raise RuntimeError(f"Error verifying payment: {e}")

        if v_resp.state != "OK":
            raise ValueError(f"Payment verification failed with status: {v_resp.state}")

        return v_resp
    def process_payment(self, t: Transaction, v_resp: CallbackResponse) -> CallbackResponse:
        # Update the transaction state to SUCCESS
        successTran = t.model_copy(update={"state":TransactionState.SUCCESS,
            "updated_at":datetime.now(),}
        )
        try:
            sTran = self.repo.upsert_transaction(successTran)
        except Exception as e:
            raise RuntimeError(f"Failed to update transaction: {e}")

        # Update the wallet balance
        try:
            new_balance = self.repo.update_balance(sTran.wallet_id, sTran.amount)
        except Exception as e:
            raise RuntimeError(f"Failed to update wallet balance: {e}")

        return CallbackResponse(
            amount=sTran.amount,
            ref_id=sTran.ref_id,
            card_pan=sTran.card_pan,
            hash_card=sTran.hash_card,
            state=sTran.state,
            processed_at=sTran.updated_at,
        )
