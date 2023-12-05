from django.contrib import admin
from .models import (
    Category,
    Product,
    ProductAttribute,
    ProductType,
    Brand,
    ProductAttributeValue,
    ProductInventory,
    Media,
    Stock,
    ProductAttributeValues,
    ProductTypeAttribute,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "parent")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "web_id", "slug", "is_active", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("category",)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ("product_attribute", "attribute_value")


@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "upc",
        "product",
        "brand",
        "is_active",
        "is_default",
        "retail_price",
        "store_price",
        "sale_price",
        "weight",
        "created_at",
        "updated_at",
    )
    filter_horizontal = ("attribute_values",)


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = (
        "product_inventory",
        "image",
        "alt_text",
        "is_feature",
        "created_at",
        "updated_at",
    )


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("product_inventory", "last_checked", "units", "units_sold")


@admin.register(ProductAttributeValues)
class ProductAttributeValuesAdmin(admin.ModelAdmin):
    list_display = ("attributevalues", "productinventory")


@admin.register(ProductTypeAttribute)
class ProductTypeAttributeAdmin(admin.ModelAdmin):
    list_display = ("product_attribute", "product_type")
