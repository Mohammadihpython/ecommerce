from django.urls import reverse
from rest_framework import status


def test_search_product_inventory_view(db, api_client, product_inventory_factory):
    # Create a product inventory using the factory
    for _ in range(2):
        product_inventory_factory.create()

    query = "Product"  # Replace with your actual search query
    url = (
        reverse("search:search_product") + f"?query={query}"
    )  # Replace with your URL name
    response = api_client.get(url)

    # Assert the response status code is HTTP 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Assert the expected product is present in the response
    # assert product_inventory.product.name in response.data
