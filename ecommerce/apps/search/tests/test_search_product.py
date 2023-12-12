import pytest
from django.urls import reverse
from rest_framework import status

from ecommerce.tests.factories import AttributeValueFactory


@pytest.mark.django_db
def test_search_product_inventory_view(
    db, api_client, product_inventory_factory, wait_for_elasticsearch
):
    attribute_values = AttributeValueFactory.create_batch(5)
    product_inventory_factory.create(attribute_values=attribute_values)

    query = "Product"
    url = reverse("search:product") + f"?search={query}"
    response = api_client.get(url)

    # Assert the response status code is HTTP 200 OK
    assert response.status_code == status.HTTP_200_OK
