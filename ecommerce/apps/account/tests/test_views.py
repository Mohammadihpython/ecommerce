from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserDetailUpdateDeleteView:
    def test_get_user_detail(self, db, user_factory, authenticated_client):
        superuser = user_factory.create(is_superuser=True, is_staff=True)
        client = authenticated_client(superuser)
        url = reverse("account:users-detail", kwargs={"pk": superuser.pk})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_update_user_detail(self, db, user_factory, authenticated_client):
        superuser = user_factory.create(is_superuser=True, is_staff=True)
        print(superuser.first_name)
        client = authenticated_client(superuser)
        url = reverse("account:users-detail", kwargs={"pk": superuser.pk})
        update_data = {
            # "phone_number": "989933642792",
            "first_name": "Hamed",
            "last_name": "Mohammadi",
        }

        response = client.put(url, data=update_data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_delete_user(self, db, user_factory, authenticated_client):
        superuser = user_factory.create(is_superuser=True, is_staff=True)
        print(superuser.first_name)
        client = authenticated_client(superuser)

        url = reverse("account:users-detail", kwargs={"pk": superuser.pk})
        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_user_list_view(db, user_factory, authenticated_client):
    superuser = user_factory.create(is_superuser=True, is_staff=True)
    client = authenticated_client(superuser)
    # url = reverse('account: ')
    response = client.get("/account/")
    response.status_code = status.HTTP_200_OK


@pytest.mark.django_db
class TestUserProfileView:
    def test_get_user_profile(self, user_factory, authenticated_client):
        user = user_factory.create()
        client = authenticated_client(user)
        url = reverse("account:user-profile")
        response = client.get(url)
        response.status_code = status.HTTP_200_OK

    def test_update_profile(self, user_factory, authenticated_client):
        user = user_factory.create()
        client = authenticated_client(user)
        url = reverse("account:user-profile")
        updated_data = {"first_name": "Ali", "last_name": "Mohammadi"}
        response = client.put(url, data=updated_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        db_user = (
            get_user_model().objects.filter(phone_number=user.phone_number).first()
        )
        assert db_user.first_name == "Ali"  # type: ignore


@pytest.mark.django_db
def test_login_view(db, user_factory, api_client):
    user = user_factory.create()
    client = api_client

    url = reverse("account:login")
    response = client.post(url, data={"phone_number": user.phone_number})
    assert response.status_code == status.HTTP_200_OK
    assert "otp" in response.data  # Check if 'otp' is present in the response data


@pytest.mark.django_db
def test_verify_otp_view_with_redis_cache(user_factory, api_client):
    client = api_client
    login_url = reverse("account:login")
    verify_url = reverse("account:verify")

    # Create a user
    user = user_factory.create()

    # Make POST request to LoginView to generate OTP
    login_data = {"phone_number": user.phone_number}
    login_response = client.post(login_url, data=login_data, format="json")

    assert login_response.status_code == status.HTTP_200_OK
    assert "otp" in login_response.data

    otp_code = login_response.data["otp"]

    # Prepare data for the request to VerifyOtpView
    data = {"code": otp_code}
    # Make POST request to VerifyOtpView
    response = client.post(verify_url, data=data, format="json")

    # Validate response
    assert response.status_code == status.HTTP_200_OK
    assert response.data["access"]


@pytest.mark.django_db
def test_verify_otp_view_with_mock_cache(api_client, user_factory):
    with patch("ecommerce.apps.account.api.views.cache") as mocked_cache:
        # Simulate the cache behavior
        user = user_factory.create()
        mocked_cache.get.side_effect = lambda key: {
            "127.0.0.1-for-authentication": user.phone_number,
            user.phone_number: "123456",
        }.get(key)

        client = api_client
        data = {"code": "123456"}  # Assuming this is the code being sent in the request

        verify_url = reverse("account:verify")

        response = client.post(verify_url, data=data)

        # Validate response
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_verify_otp_view_and_register_user(api_client, user_factory):
    with patch("ecommerce.apps.account.api.views.cache") as mocked_cache:
        # Simulate the cache behavior
        user = user_factory.build()
        mocked_cache.get.side_effect = lambda key: {
            "127.0.0.1-for-authentication": user.phone_number,
            user.phone_number: "123456",
        }.get(key)
        client = api_client
        register_url = reverse("account:register")

        register_response = client.post(
            register_url, data={"phone_number": user.phone_number}, format="json"
        )
        assert register_response.status_code == status.HTTP_200_OK

        data = {"code": "123456"}  # Assuming this is the code being sent in the request

        verify_url = reverse("account:verify")

        response = client.post(verify_url, data=data)
        # Validate response
        assert response.status_code == status.HTTP_200_OK
