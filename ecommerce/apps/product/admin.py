from django.contrib import admin

from . import models

# Register your models here.


admin.site.register(models.Category)
admin.site.register(models.Brand)
admin.site.register(models.Media)
admin.site.register(models.Product)
admin.site.register(models.ProductAttribute)
admin.site.register(models.ProductAttributeValue)
admin.site.register(models.ProductAttributeValues)
admin.site.register(models.ProductType)
admin.site.register(models.ProductInventory)
