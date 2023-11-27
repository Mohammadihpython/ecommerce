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
