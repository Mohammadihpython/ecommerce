import pytest
from django.urls import reverse
from rest_framework import status

from ecommerce.apps.product.endpoints.serializers import ProductSerializer


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


@pytest.mark.django_db
class TestProductViewSet:
    def test_product_detail(
        self, db, authenticated_client, product_factory, user_factory
    ):
        superuser = user_factory.create(is_superuser=True, is_staff=True)
        client = authenticated_client(superuser)
        product_detail = product_factory.create()
        url = reverse(
            "product-detail",
            kwargs={"pk": product_detail.pk},
        )
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_product_list(
        self, db, product_factory, authenticated_client, user_factory
    ):
        superuser = user_factory.create(is_superuser=True, is_staff=True)
        client = authenticated_client(superuser)
        # create products
        product_factory.create_batch(40)
        # test get data
        url = reverse("product-list")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_product_create(
        self, authenticated_client, user_factory, product_factory, category_factory
    ):
        # create an authenticated user
        superuser = user_factory.create(is_superuser=True, is_staff=True)
        client = authenticated_client(superuser)

        # create a new product data
        categories = category_factory.create_batch(5)
        product = product_factory.stub(category=categories)
        serializer = ProductSerializer(instance=product)
        new_product = dict(serializer.data)
        new_product["category"] = [category.id for category in categories]

        # get url of view
        url = reverse("product-list")
        # send new product to create them
        response = client.post(url, data=new_product, format="json")

        assert response.status_code == status.HTTP_201_CREATED

    def test_product_delete(
        self, db, product_factory, user_factory, authenticated_client
    ):
        superuser = user_factory.create(is_superuser=True, is_staff=True)
        client = authenticated_client(superuser)
        product_detail = product_factory.create()
        url = reverse(
            "product-detail",
            kwargs={"pk": product_detail.pk},
        )
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestProductInventoryViewSet:
    def test_inventory_detail(
        self,
        db,
        authenticated_client,
        product_inventory_factory,
        user_factory,
        media_factory,
        wait_for_elasticsearch,
    ):
        superuser = user_factory.create(is_superuser=True, is_staff=True)
        client = authenticated_client(superuser)
        inventory_product = product_inventory_factory.create()
        media_factory.create(product_inventory=inventory_product)

        url = reverse(
            "productinventory-detail",
            kwargs={"pk": inventory_product.pk},
        )
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_inventory_list(
        self, db, product_factory, authenticated_client, user_factory
    ):
        superuser = user_factory.create(is_superuser=True, is_staff=True)
        client = authenticated_client(superuser)
        # create products
        product_factory.create_batch(40)
        # test get data
        url = reverse("product-list")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_inventory_create(
        self,
        authenticated_client,
        user_factory,
        product_factory,
        product_type_factory,
        product_inventory_factory,
        brand_factory,
        media_factory,
        wait_for_elasticsearch,
    ):
        # create an authenticated user
        superuser = user_factory.create(is_superuser=True, is_staff=True)
        client = authenticated_client(superuser)

        # create a new product data

        inventory = product_inventory_factory.stub()
        product = product_factory.create()
        brand = brand_factory.create()
        product = product_factory.create()
        product_type = product_type_factory.create()
        new_product = {
            "sku": inventory.sku,
            "upc": inventory.upc,
            "product": product.id,
            "product_type": product_type.id,
            "brand": brand.id,
            "is_active": True,
            "is_default": True,
            "retail_price": 999.99,
            "store_price": 999.99,
            "sale_price": 999.99,
            "weight": 22.6,
        }

        # get url of view
        url = reverse("productinventory-list")
        # send new product to create them
        response = client.post(url, data=new_product, format="json")

        assert response.status_code == status.HTTP_201_CREATED

    def test_product_delete(
        self, db, product_factory, user_factory, authenticated_client
    ):
        superuser = user_factory.create(is_superuser=True, is_staff=True)
        client = authenticated_client(superuser)
        product_detail = product_factory.create()
        url = reverse(
            "product-detail",
            kwargs={"pk": product_detail.pk},
        )
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
