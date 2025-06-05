"""
here are some more options that you can use with factory.Faker to generate random values:
word: Generates a random word.
sentence: Generates a random sentence.
paragraph: Generates a random paragraph.
text: Generates a random text.
ipv4: Generates a random IPv4 address.
ipv6: Generates a random IPv6 address.
mac_address: Generates a random MAC address.
user_name: Generates a random username.
password: Generates a random password.
url: Generates a random URL.
slug: Generates a random slug.
color: Generates a random color.
file_name: Generates a random file name.
file_path: Generates a random file path.
mime_type: Generates a random MIME type.
credit_card_number: Generates a random credit card number.
credit_card_expire: Generates a random credit card expiration date.
credit_card_security_code: Generates a random credit card security code.
ssn: Generates a random social security number.
isbn13: Generates a random ISBN-13 number.
ean13: Generates a random EAN-13 number.
ean8: Generates a random EAN-8 number.
isbn10: Generates a random ISBN-10 number.
currency_code: Generates a random currency code.
currency_name: Generates a random currency name.
currency_symbol: Generates a random currency symbol.
first_name: Generates a random first name.
last_name: Generates a random last name.
name: Generates a random full name.
email: Generates a random email address.
phone_number: Generates a random phone number.
date: Generates a random date.
time: Generates a random time.
address: Generates a random address.
city: Generates a random city name.
state: Generates a random state name.
zip_code: Generates a random zip code.
country: Generates a random country name.
latitude: Generates a random latitude value.
longitude: Generates a random longitude value.
random_int: Generates a random integer.
random_digit: Generates a random digit.
random_letter: Generates a random letter.
random_element: Generates a random element from a list.
random_sample: Generates a random sample of elements from a list.
"""

from datetime import datetime

import factory
from django.contrib.auth import get_user_model
from faker import Faker
from pytest_factoryboy import register

from ecommerce.apps.cart.models import Cart
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

    id = factory.Sequence(lambda n: n + 1)
    id = factory.Sequence(lambda n: n + 1)
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

    name = factory.Sequence(lambda n: f"type-{n + 1}")


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
    web_id = factory.Sequence(lambda n: f"{n + 2}")
    slug = factory.Faker("slug")
    name = factory.Sequence(lambda n: f"product-{n + 1}")
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

    id = factory.Sequence(lambda n: n + 1)
    sku = factory.Sequence(lambda n: f"SKU-{n + 1}")
    upc = factory.Sequence(lambda n: f"UPC-{n + 1}")

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


# cart factory
@register
class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    product = factory.SubFactory(ProductInventoryFactory)
    quantity = factory.Faker("random_int", min=0)
