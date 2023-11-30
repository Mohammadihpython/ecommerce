from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from ..product import models
from ..product.documents import ProductInventoryDocument


@receiver(post_save, sender=models.ProductInventory)
def update_product_inventory_document(sender, instance, **kwargs):
    ProductInventoryDocument().update(instance)


@receiver(post_delete, sender=models.ProductInventory)
def remove_product_inventory_document(sender, instance, **kwargs):
    ProductInventoryDocument().get(id=instance.id).delete()
