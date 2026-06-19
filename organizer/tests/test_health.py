from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


def test_health_check_returns_ok() -> None:
    """The health endpoint exposes a minimal success payload."""
    client = APIClient()

    response = client.get(reverse("organizer:health"))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
