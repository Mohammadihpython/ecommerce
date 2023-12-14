from datetime import datetime

import factory
from django.contrib.auth import get_user_model
from faker import Faker
from pytest_factoryboy import register

from ecommerce.apps.product.models import (
    Brand,
    Category,
    Media,
    Product,
    ProductAttribute,
    ProductAttributeValue,
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

    id = factory.Sequence(lambda n: n + 1)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone_number = factory.Sequence(lambda n: f"989{str(n).zfill(9)}")


# product factory


@register
class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand
        django_get_or_create = ["id"]

    id = factory.Sequence(lambda n: n + 1)

    name = factory.Faker("company")


@register
class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    id = factory.Sequence(lambda n: n + 1)

    name = factory.Sequence(lambda n: f"type-{n+1}")


@register
class ProductAttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttribute
        django_get_or_create = ["name"]

    id = factory.Sequence(lambda n: n + 1)

    name = factory.Faker("word")
    description = factory.Faker("sentence")


@register
class AttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttributeValue

    id = factory.Sequence(lambda n: n + 1)

    product_attribute = factory.SubFactory(ProductAttributeFactory)
    attribute_value = factory.Faker("word")


@register
class CategoryFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker("word")
    slug = factory.Faker("slug")
    is_active = True

    class Meta:
        model = Category
        django_get_or_create = ["name"]


@register
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        django_get_or_create = ["web_id"]
        skip_postgeneration_save = True

    id = factory.Sequence(lambda n: n + 1)
    web_id = factory.Sequence(lambda n: f"{n+2}")
    slug = factory.Faker("slug")
    name = factory.Sequence(lambda n: f"product-{n+1}")
    description = factory.Faker("text")
    is_active = True

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of categories were passed in, use them
            for category in extracted:
                self.category.add(category)  # type: ignore


@register
class ProductInventoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductInventory

    sku = factory.Sequence(lambda n: f"SKU-{n+1}")
    upc = factory.Sequence(lambda n: f"UPC-{n+1}")

    product_type = factory.SubFactory(ProductTypeFactory)
    brand = factory.SubFactory(BrandFactory)
    is_active = True
    is_default = True
    retail_price = 999.99
    store_price = 999.99
    sale_price = 999.99
    weight = 22.6

    @factory.post_generation
    def attribute_values(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        for attribute_values in extracted:
            self.attribute_values.add(attribute_values)  # type: ignore

    @factory.lazy_attribute
    def product(self):
        categories = CategoryFactory.create_batch(3)  # Create 3 categories
        # Create a product using the ProductFactory
        return ProductFactory(category=categories)


@register
class MediaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Media

    product_inventory = factory.SubFactory(ProductInventoryFactory)
    image = factory.django.ImageField(filename="example_image.jpg")
    alt_text = factory.Faker("sentence", nb_words=6)
    is_feature = factory.Faker("boolean")
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)


ProductInventoryFactory
