import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client():
    def _create_client(user):
        token = str(AccessToken.for_user(user))
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return client

    return _create_client
