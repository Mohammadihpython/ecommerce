from rest_framework import serializers

from ecommerce.apps.product.models import ProductAttributeValues  # type: ignore
from ecommerce.apps.product.models import (
    Brand,
    Category,
    Media,
    Product,
    ProductAttribute,
    ProductAttributeValue,
    ProductInventory,
    ProductType,
    ProductTypeAttribute,
    Stock,
)


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        # fields = "__all__"
        depth = 2
        exclude = ["id"]


class MediaSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = ["img_url", "alt_text"]
        read_only = True
        editable = False

    def get_img_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.image.url)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["name"]


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["name", "description"]


class ProductTypeSerializer(serializers.ModelSerializer):
    product_type_attribute = ProductAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = ProductType
        fields = ["name", "product_type_attribute"]


class ProductTypeAttributeSerializer(serializers.ModelSerializer):
    product_attribute = ProductAttributeSerializer(many=False)
    product_type = ProductTypeSerializer(many=False)

    class Meta:
        model = ProductTypeAttribute
        fields = ["product_type", "product_attribute"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ["slug", "name", "description", "category"]
        read_only = True
        editable = False


class StockSerializer(serializers.ModelSerializer):
    product_inventory = "ProductInventorySerializer"

    class Meta:
        model = Stock
        fields = ["product_inventory", "units", "units_sold", "last_checked"]


class ProductInventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    media_product_inventory = MediaSerializer(many=True, read_only=True)
    product_type = ProductTypeSerializer(many=False, read_only=True)
    brand = BrandSerializer(many=False, read_only=True)
    attribute_values = ProductAttributeValueSerializer(many=True, read_only=True)
    stock = StockSerializer(many=True, read_only=True)

    class Meta:
        model = ProductInventory
        fields = [
            "id",
            "store_price",
            "is_default",
            "retail_price",
            "product",
            "media_product_inventory",
            "product_type",
            "brand",
            "attribute_values",
            "stock",
        ]
        read_only = True


class ProductAttributeValuesSerializer(serializers.ModelSerializer):
    attributevalues = ProductAttributeValueSerializer(many=False)
    productinventory = ProductInventorySerializer(many=False)

    class Meta:
        model = ProductAttributeValues
        fields = ["attributevalues", "productinventory"]


class ProductInventoryLightSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    media_product_inventory = MediaSerializer(many=True, read_only=True)
    product_type = ProductTypeSerializer(many=False, read_only=True)
    brand = BrandSerializer(many=False, read_only=True)
    attribute_values = ProductAttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductInventory
        fields = [
            "id",
            "store_price",
            "is_default",
            "retail_price",
            "product",
            "media_product_inventory",
            "product_type",
            "brand",
            "attribute_values",
        ]
        read_only = True
