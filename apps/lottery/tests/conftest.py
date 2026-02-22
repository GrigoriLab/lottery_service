from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.lottery.models import Ballot, Lottery

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", email="test@example.com", password="secure_password")


@pytest.fixture
def second_user(db):
    return User.objects.create_user(username="testuser2", email="test2@example.com", password="secure_password")


@pytest.fixture
def active_lottery(db):
    return Lottery.objects.create(status=Lottery.Status.ACTIVE, expires_at=timezone.now() + timedelta(days=1))


@pytest.fixture
def finished_lottery(db):
    return Lottery.objects.create(status=Lottery.Status.FINISHED, expires_at=timezone.now() - timedelta(days=1))


@pytest.fixture
def draft_lottery(db):
    return Lottery.objects.create(status=Lottery.Status.DRAFT, expires_at=timezone.now() + timedelta(days=1))


@pytest.fixture
def ballot(active_lottery, user):
    return Ballot.objects.create(lottery=active_lottery, participant=user)
