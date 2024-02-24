from django.contrib.auth import get_user_model
from rest_framework import serializers

from ecommerce.apps.product.models import ProductInventory

from ..models import Cart

User = get_user_model()


class CartSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=ProductInventory.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Cart
        fields = ["user", "product", "quantity"]
