from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Any

from django.db import IntegrityError, connection, transaction

from ecommerce.apps.wallet.models import Wallet
from ecommerce.apps.wallet.service import Repository

from ..models import Transaction
from ..types import Transaction as TransactionType
from ..types import TransactionState


class WalletRepo(Repository):
    @staticmethod
    def create_wallet(user_id: int) -> int:
        """Creates a wallet for a given user_id and returns the wallet ID."""
        try:
            wallet = Wallet.objects.create(user_id=user_id, balance=0)
            return wallet.pk  # Use the primary key attribute
        except IntegrityError as e:
            if (
                "unique constraint" in str(e).lower()
            ):  # Handling duplicate wallet creation
                raise ValueError("Wallet already exists for this user.")
            raise RuntimeError(f"Failed to create wallet: {e}")

    def get_wallet_by_user_id(self, user_id: int) -> int:
        """Retrieve the wallet for the user with the given user_id."""
        wallet = Wallet.objects.get(user_id=user_id)
        return wallet.pk

    def upsert_transaction(self, transaction: TransactionType) -> TransactionType:
        """Insert or update a transaction in the database."""
        defaults = {
            "wallet_id": transaction.wallet_id,
            "amount": transaction.amount,
            "state": transaction.state.value,
            "updated_at": transaction.updated_at,
        }

        if transaction.card_pan is not None:
            defaults["card_pan"] = transaction.card_pan
        if transaction.hash_card is not None:
            defaults["hash_card"] = transaction.hash_card
        if transaction.ref_id is not None:
            defaults["ref_id"] = transaction.ref_id
        if transaction.created_at is not None:
            defaults["created_at"] = transaction.created_at
        try:
            obj, _ = Transaction.objects.update_or_create(
                id=transaction.id,
                defaults=defaults,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to upsert Transaction: {e}")
        return TransactionType(
            id=obj.pk,
            wallet_id=obj.wallet,
            amount=obj.amount,
            state=TransactionState(obj.state),
            authority=obj.authority,
            card_pan=obj.card_pan,
            hash_card=obj.hash_card,
            ref_id=obj.ref_id,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )

    def update_balance(self, wallet_id: int, amount: int) -> int:
        """Update the balance of the wallet with the given wallet_id."""
        try:
            wallet = Wallet.objects.select_for_update().get(id=wallet_id)
            wallet.balance += amount
            wallet.save()
            return wallet.balance
        except Wallet.DoesNotExist:
            raise ValueError(f"Wallet with ID {wallet_id} does not exist.")
        except Exception as e:
            raise RuntimeError(f"Failed to update balance: {e}")

    def get_wallet_balance(self, wallet_id: int) -> int:
        """Retrieve the balance of the wallet with the given wallet_id."""
        try:
            wallet = Wallet.objects.get(id=wallet_id)
            return wallet.balance
        except Wallet.DoesNotExist:
            raise ValueError(f"Wallet with ID {wallet_id} does not exist.")
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve wallet balance: {e}")

    def get_transaction_by_authority(self, authority: str) -> TransactionType:
        """Retrieve a transaction by its authority."""
        try:
            transaction = Transaction.objects.get(authority=authority)
            return TransactionType(
                id=transaction.pk,
                wallet_id=transaction.wallet,
                amount=transaction.amount,
                state=TransactionState(transaction.state),
                authority=transaction.authority,
                card_pan=transaction.card_pan,
                hash_card=transaction.hash_card,
                ref_id=transaction.ref_id,
                created_at=transaction.created_at,
                updated_at=transaction.updated_at,
            )
        except Transaction.DoesNotExist:
            raise ValueError(f"Transaction with authority {authority} does not exist.")
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve transaction: {e}")

    @staticmethod
    def transaction_lock(wallet_id: int, fun: Callable[[], Any]):
        """Lock the transaction for the given wallet_id and execute the function."""
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT 1 FROM wallet WHERE wallet_id = %s FOR UPDATE NOWAIT",
                        [wallet_id],
                    )
                    result = fun()
                    return result
        except Exception as e:
            raise RuntimeError(
                f"Transaction lock failed for wallet_id {wallet_id}: {e}"
            )

    @staticmethod
    def review_transaction() -> None:
        """Review a transaction and update its state. Cancel transactions that are pending for more than 12 hours."""
        tow_elv_hour_ago = datetime.now() - timedelta(hours=12)
        try:
            Transaction.objects.filter(
                state=TransactionState.PENDING, created_at__lt=tow_elv_hour_ago
            ).update(state=TransactionState.CANCELLED)
        except Exception as e:
            print(f"Error reviewing transactions: {e}")
            # Handle the exception as needed, e.g., log it or raise a custom exception
