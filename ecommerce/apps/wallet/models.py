from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
User = get_user_model()


class Wallet(models.Model):
    user_id = models.OneToOneField(
        User, related_name="wallet", on_delete=models.CASCADE
    )
    balance = models.BigIntegerField(verbose_name=_("balance"), default=0)
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("date balance created"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("date balance last updated"),
        help_text=_("format: Y-m-d H:M:S"),
    )

    def __str__(self):
        return f"{self.user_id}-{self.balance}"


class Transaction(models.Model):
    class TransactionState(models.TextChoices):
        StatePending = "pending", _("pending")
        StateComplete = "complete", _("complete")
        stateFailed = "failed", _("failed")
        StateCanceled = "canceled", _("canceled")

    wallet = models.ForeignKey(
        Wallet, verbose_name="transactions", on_delete=models.PROTECT
    )
    amount = models.BigIntegerField(_("amount of transaction"))
    state = models.CharField(max_length=10, choices=TransactionState)
    authority = models.TextField(verbose_name=_("authority of transaction"))
    card_pan = models.CharField(
        max_length=20, verbose_name=_("card pan"), blank=True, null=True
    )
    hash_card = models.CharField(
        max_length=190, verbose_name=_("hash card "), blank=True, null=True
    )
    ref_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("date balance created"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("date balance last updated"),
        help_text=_("format: Y-m-d H:M:S"),
    )

    def __str__(self):
        return f"{self.wallet}-{self.state}"
