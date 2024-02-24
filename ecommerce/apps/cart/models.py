from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..product.models import ProductInventory

# Create your models here.

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, related_name="cards", on_delete=models.PROTECT)
    product = models.ForeignKey(ProductInventory, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(_("تعداد"))
