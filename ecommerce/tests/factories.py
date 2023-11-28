import factory
from django.contrib.auth import get_user_model
from faker import Faker
from pytest_factoryboy import register

from ecommerce.apps.product.models import (
    Brand,
    Category,
    Product,
    ProductAttribute,
    ProductInventory,
    ProductType,
)

User = get_user_model()
fake = Faker("fa_IR")


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    is_superuser = False
    is_staff = False
    phone_number = factory.Sequence(lambda n: f"989{str(n).zfill(9)}")


@register
class UpdateUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone_number = factory.Sequence(lambda n: f"989{str(n).zfill(9)}")


# product factory


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Faker("company")


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = factory.Faker("word")


class ProductAttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttribute

    name = factory.Faker("word")
    description = factory.Faker("sentence")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    slug = factory.Faker("slug")
    is_active = True


@register
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    web_id = factory.Sequence(lambda n: f"{n+1}")
    slug = factory.Faker("slug")
    name = factory.Sequence(lambda n: f"product-{n+1}")
    description = factory.Faker("text")
    is_active = True


@register
class ProductInventoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductInventory

    sku = factory.Sequence(lambda n: f"SKU-{n+1}")
    upc = factory.Sequence(lambda n: f"UPC-{n+1}")
    product_type = factory.SubFactory(ProductTypeFactory)
    product = factory.SubFactory(ProductFactory)
    brand = factory.SubFactory(BrandFactory)
    is_active = True
    is_default = True
    retail_price = 999.99
    store_price = 999.99
    sale_price = 999.99
    weight = 22.6
