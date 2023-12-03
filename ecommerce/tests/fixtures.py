import contextlib
import time

import pytest
import requests
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


# Fixture to check Elasticsearch availability
@pytest.fixture(scope="session")
def wait_for_elasticsearch():
    max_retries = 3
    for _ in range(max_retries):
        with contextlib.suppress(requests.ConnectionError):
            # Attempt to connect to Elasticsearch
            response = requests.get(
                "http://es:9200"
            )  # Replace with your Elasticsearch URL
            if response.status_code == 200:
                return  # If successful, return immediately
        # Wait for a brief moment before the next retry
        time.sleep(5)
    # If Elasticsearch is not available after the maximum retries, raise an error
    raise RuntimeError("Elasticsearch is not available")
