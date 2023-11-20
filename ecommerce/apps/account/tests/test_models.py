
import pytest


@pytest.mark.django_db
def test_user_model_phone_number_regex_validator(db,django_user_model,user_factory):
    user_test = user_factory.create()
    user = django_user_model.objects.create(
        phone_number = user_factory.phone_number

    )


