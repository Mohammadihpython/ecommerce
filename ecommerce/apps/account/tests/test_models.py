
import pytest


def test_create_user(db,django_user_model,user_factory):
    django_user_model.objects.create(
        phone_number=user_factory.phone_number,
        password = user_factory.password
        )
