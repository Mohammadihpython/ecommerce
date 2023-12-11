import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_product_by_category_view(db, api_client, product_factory, category_factory):
    categories = category_factory.create_batch(3)
    product = product_factory.create(category=categories)
    params = {"category_slug": categories[0].slug}

    url = reverse("by-category-detail", kwargs=params)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["slug"] == product.slug


@pytest.mark.django_db
def test_all_products_view(
    db,
    api_client,
    product_factory,
):
    products = product_factory.create_batch(20)

    list_products_url = reverse("all-products-list")
    response = api_client.get(list_products_url)
    assert response.status_code == status.HTTP_200_OK

    get_product_url = reverse("all-products-detail", kwargs={"slug": products[0].slug})
    response = api_client.get(get_product_url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_inventory_products_by_product_id(
    db, api_client, product_inventory_factory, wait_for_elasticsearch, media_factory
):
    inventory_product = product_inventory_factory.create()
    media_factory.create(product_inventory=inventory_product)

    list_products_url = reverse(
        "inventory-products-by-productID-detail",
        kwargs={"productId": inventory_product.product.id},
    )
    response = api_client.get(list_products_url)
    assert response.status_code == status.HTTP_200_OK
