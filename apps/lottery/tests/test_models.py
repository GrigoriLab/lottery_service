from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils import timezone

from apps.lottery.models import Ballot, Lottery, Winner

User = get_user_model()


@pytest.mark.django_db
class TestLotteryModel:
    def test_str(self, active_lottery):
        assert str(active_lottery) == f"Lottery {active_lottery.id} (active)"

    def test_str_draft(self, draft_lottery):
        assert str(draft_lottery) == f"Lottery {draft_lottery.id} (draft)"

    def test_default_status_is_draft(self, db):
        lottery = Lottery.objects.create(expires_at=timezone.now() + timedelta(days=1))
        assert lottery.status == Lottery.Status.DRAFT

    def test_ordering_by_created_at_desc(self, db):
        first = Lottery.objects.create(expires_at=timezone.now() + timedelta(days=1))
        second = Lottery.objects.create(expires_at=timezone.now() + timedelta(days=2))
        lotteries = list(Lottery.objects.all())
        assert lotteries == [second, first]


@pytest.mark.django_db
class TestBallotModel:
    def test_str(self, ballot):
        assert str(ballot) == f"Ballot by {ballot.participant}(lottery={ballot.lottery.id})"

    def test_lottery_relationship(self, ballot):
        assert ballot in ballot.lottery.ballots.all()

    def test_participant_relationship(self, ballot):
        assert ballot in ballot.participant.ballots.all()

    def test_ordering_by_submitted_at_desc(self, active_lottery, user, second_user):
        first = Ballot.objects.create(lottery=active_lottery, participant=user)
        second = Ballot.objects.create(lottery=active_lottery, participant=second_user)
        ballots = list(Ballot.objects.all())
        assert ballots == [second, first]


@pytest.mark.django_db
class TestWinnerModel:
    def test_str(self, db):
        user = User.objects.create_user(username="winner_user", password="pass12345")
        lottery = Lottery.objects.create(status=Lottery.Status.FINISHED, expires_at=timezone.now() - timedelta(days=1))
        ballot = Ballot.objects.create(lottery=lottery, participant=user)
        winner = Winner.objects.create(lottery=lottery, ballot=ballot, participant=user)
        assert str(winner) == f"Winner: {user} for {lottery.id} lottery"

    def test_lottery_one_to_one(self, db):
        user = User.objects.create_user(username="u1", password="pass12345")
        lottery = Lottery.objects.create(status=Lottery.Status.FINISHED, expires_at=timezone.now() - timedelta(days=1))
        ballot = Ballot.objects.create(lottery=lottery, participant=user)
        Winner.objects.create(lottery=lottery, ballot=ballot, participant=user)
        ballot2 = Ballot.objects.create(lottery=lottery, participant=user)
        with pytest.raises(IntegrityError):
            Winner.objects.create(lottery=lottery, ballot=ballot2, participant=user)

    def test_ballot_one_to_one(self, db):
        user = User.objects.create_user(username="u1", password="pass12345")
        lottery1 = Lottery.objects.create(status=Lottery.Status.FINISHED, expires_at=timezone.now() - timedelta(days=1))
        lottery2 = Lottery.objects.create(status=Lottery.Status.FINISHED, expires_at=timezone.now() - timedelta(days=1))
        ballot = Ballot.objects.create(lottery=lottery1, participant=user)
        Winner.objects.create(lottery=lottery1, ballot=ballot, participant=user)
        with pytest.raises(IntegrityError):
            Winner.objects.create(lottery=lottery2, ballot=ballot, participant=user)

    def test_winner_accessible_from_lottery(self, db):
        user = User.objects.create_user(username="u1", password="pass12345")
        lottery = Lottery.objects.create(status=Lottery.Status.FINISHED, expires_at=timezone.now() - timedelta(days=1))
        ballot = Ballot.objects.create(lottery=lottery, participant=user)
        winner = Winner.objects.create(lottery=lottery, ballot=ballot, participant=user)
        assert lottery.winner == winner

    def test_participant_wins_relationship(self, db):
        user = User.objects.create_user(username="u1", password="pass12345")
        lottery = Lottery.objects.create(status=Lottery.Status.FINISHED, expires_at=timezone.now() - timedelta(days=1))
        ballot = Ballot.objects.create(lottery=lottery, participant=user)
        winner = Winner.objects.create(lottery=lottery, ballot=ballot, participant=user)
        assert winner in user.wins.all()
