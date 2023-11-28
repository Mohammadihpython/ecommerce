from rest_framework import serializers

from ..product.models import Product, ProductInventory


class SearchProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "slug",
            "name",
            "web_id",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        fields = [
            "name",
        ]
        read_only = True
        editable = False


class SearchProductInventorySerializer(serializers.ModelSerializer):
    product = SearchProductSerializer(many=False, read_only=True)

    class Meta:
        model = ProductInventory
        fields = [
            "id",
            "retail_price",
            "store_price",
            "sale_price",
            "weight",
            "created_at",
            "updated_at",
        ]
        read_only = True
