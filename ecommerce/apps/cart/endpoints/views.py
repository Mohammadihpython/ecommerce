from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ...product.models import ProductInventory
from ..models import Cart
from .serializers import CartSerializer


class AddCartView(GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]


    @transaction.atomic
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        product_id = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        # use select for update to lock this row
        product = ProductInventory.objects.select_for_update().get(id=product_id)
        # TODO Check if product Stock is empty did not create add to cart
        if product.stock < quantity:  # type: ignore
            raise ValidationError("Insufficient stock for this product.")

        Cart.objects.create(
            user_id=user.id,
            product_id=product.id,  # type: ignore
            quantity=quantity,
        )
        product.stock.units -= quantity  # type: ignore
        product.save()  # Save the updated product count

        context = {"success": "added to cart."}
        return Response(context, status=status.HTTP_201_CREATED)


class DelCartView(GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request):  # sourcery skip: extract-method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        product_id = serializer.validated_data["product_id"]
        try:
            cart_item = Cart.objects.get(user_id=user.id, product_id=product_id)
            # increase amount of product
            product = cart_item.product
            product.stock.units += cart_item.quantity  # type: ignore
            product.save()
            # remove product from user cart lists
            cart_item.delete()

            context = {"success": "remove from cart."}
            return Response(context, status=status.HTTP_200_OK)
        except ProductInventory.DoesNotExist or Cart.DoesNotExist:
            context = {"error": "Product matching query not exists"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
