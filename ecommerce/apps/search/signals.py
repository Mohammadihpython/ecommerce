from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from ..product import models
from . import product_documents


@receiver(post_save, sender=models.ProductInventory)
def update_product_inventory_document(sender, instance, **kwargs):
    product_documents.ProductInventoryDocument().update(instance)


@receiver(post_delete, sender=models.ProductInventory)
def remove_product_inventory_document(sender, instance, **kwargs):
    product_documents.ProductInventoryDocument().get(id=instance.id).delete()


@receiver(post_save, sender=models.Product)
def update_product_document(sender, instance, **kwargs):
    product_documents.ProductDocument().update(instance)


@receiver(post_delete, sender=models.Product)
def remove_product_document(sender, instance, **kwargs):
    product_documents.ProductDocument().get(id=instance.id).delete()
