import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_add_to_cart_view(
    db,
    wait_for_elasticsearch,
    user_factory,
    authenticated_client,
    product_inventory_factory,
):
    product = product_inventory_factory.create()
    user = user_factory.create()
    client = authenticated_client(user)
    data = {"user": user.id, "product": product.id, "quantity": 1}

    url = reverse("cart:add-cart")
    response = client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED
