from datetime import date

import pytest

from apps.lottery.models import Ballot


@pytest.mark.django_db
class TestRegisterView:
    def test_register(self, api_client):
        resp = api_client.post(
            "/api/v1/auth/register/",
            {"username": "newuser", "email": "new@example.com", "password": "secure_password"},
        )
        assert resp.status_code == 201
        assert resp.data["username"] == "newuser"
        assert "password" not in resp.data

    def test_register_duplicate(self, api_client, user):
        resp = api_client.post(
            "/api/v1/auth/register/",
            {"username": user.username, "email": "new@example.com", "password": "strongpass123"},
        )
        assert resp.status_code == 400


@pytest.mark.django_db
class TestTokenViews:
    def test_obtain_token(self, api_client, user):
        resp = api_client.post(
            "/api/v1/auth/token/",
            {"username": user.username, "password": "secure_password"},
        )
        assert resp.status_code == 200
        assert "access" in resp.data
        assert "refresh" in resp.data

    def test_obtain_token_wrong_password(self, api_client, user):
        resp = api_client.post(
            "/api/v1/auth/token/",
            {"username": user.username, "password": "wrong_password"},
        )
        assert resp.status_code == 401


@pytest.mark.django_db
class TestLotteryViews:
    def test_list_lotteries(self, api_client, active_lottery, finished_lottery, draft_lottery):
        resp = api_client.get("/api/v1/lotteries/")
        assert resp.status_code == 200
        assert len(resp.data) == 2


@pytest.mark.django_db
class TestBallotViews:
    def test_list_ballots(self, auth_client, active_lottery, ballot):
        resp = auth_client.get("/api/v1/ballots/")
        assert resp.status_code == 200
        assert Ballot.objects.count() == 1

    def test_create_ballot(self, auth_client, active_lottery):
        resp = auth_client.post("/api/v1/ballots/", {"lottery": active_lottery.id})
        assert resp.status_code == 201
        assert Ballot.objects.count() == 1

    def test_create_ballot_unauthenticated(self, api_client, active_lottery):
        resp = api_client.post("/api/v1/ballots/", {"lottery": active_lottery.id})
        assert resp.status_code == 401

    def test_multiple_ballots_allowed(self, auth_client, ballot):
        resp = auth_client.post("/api/v1/ballots/", {"lottery": ballot.lottery.id})
        assert resp.status_code == 201
        assert Ballot.objects.count() == 2

    def test_ballot_on_finished_lottery(self, auth_client, finished_lottery):
        resp = auth_client.post("/api/v1/ballots/", {"lottery": finished_lottery.id})
        assert resp.status_code == 400


@pytest.mark.django_db
class TestWinnerViews:
    def test_list_winners_unauthenticated(self, auth_client, winner):
        resp = auth_client.get("/api/v1/winners/")
        assert resp.status_code == 200
        assert len(resp.data) == 1

    def test_filter_winners_by_date(self, auth_client, winner):
        today = date.today().isoformat()
        resp = auth_client.get(f"/api/v1/winners/?date={today}")
        assert resp.status_code == 200
        assert len(resp.data) == 1

    def test_filter_winners_by_date_no_results(self, auth_client, winner):
        resp = auth_client.get("/api/v1/winners/?date=2000-01-01")
        assert resp.status_code == 200
        assert len(resp.data) == 0
