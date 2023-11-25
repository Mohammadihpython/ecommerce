import factory
from django.contrib.auth import get_user_model
from faker import Faker
from pytest_factoryboy import register

User = get_user_model()
fake = Faker("fa_IR")


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    phone_number = (
        phone_number
    ) = f"989{str(fake.random_int(min=100000000, max=999999999)).zfill(9)}"
