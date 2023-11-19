from django.contrib.auth import get_user_model
import faker
import factory
from faker import Faker
from pytest_factoryboy import register

user = get_user_model()
fake = Faker('fa_IR')

@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = user

    phone_number = "09191234567"
    password = "123456789"

