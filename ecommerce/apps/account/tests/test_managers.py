import pytest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from faker import Faker

from ecommerce.apps.account.managers import UserManager

fake = Faker()


@pytest.mark.django_db
def test_create_user(db, django_user_model, user_factory):
    user = user_factory.create()
    # user =django_user_model.objects.create(
    #     phone_number=factory_user.phone_number,
    #     )
    assert user.phone_number is not None


@pytest.mark.parametrize(
    "phone_number, expected", [pytest.param("234567", "شماره تلفن باید فرستاده شود")]
)
def test_failed_create_user(db, django_user_model, phone_number, expected):
    with pytest.raises(ValidationError):
        user = django_user_model.objects.create(phone_number=phone_number)
        user.full_clean()


def test_create_user_without_phone_number():
    with pytest.raises(ValueError) as e:
        manager = UserManager()
        manager.create_user(phone_number=None)  # type: ignore

    assert str(e.value) == str(_("شماره تلفن باید فرستاده شود"))


def test_create_superuser(db, django_user_model, user_factory):
    user_factory = user_factory.build()
    user = django_user_model.objects.create_superuser(
        phone_number=user_factory.phone_number, password=fake.password()
    )
    assert user.is_superuser is True
