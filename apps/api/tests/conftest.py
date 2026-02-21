from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.lottery.models import Ballot, Lottery, Winner

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="secure_password"
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(user):
    client = APIClient()
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
    return client


@pytest.fixture
def active_lottery(db):
    return Lottery.objects.create(status=Lottery.Status.ACTIVE, expires_at=date.today() + timedelta(days=1))


@pytest.fixture
def finished_lottery(db):
    return Lottery.objects.create(
        status=Lottery.Status.FINISHED, expires_at=date.today() - timedelta(days=1)
    )


@pytest.fixture
def draft_lottery(db):
    return Lottery.objects.create(
        status=Lottery.Status.DRAFT, expires_at=date.today() + timedelta(days=1)
    )


@pytest.fixture
def ballot(active_lottery, user):
    return Ballot.objects.create(lottery=active_lottery, participant=user)


@pytest.fixture
def winner(finished_lottery, user):
    ballot = Ballot.objects.create(lottery=finished_lottery, participant=user)
    return Winner.objects.create(lottery=finished_lottery, ballot=ballot, participant=user)
