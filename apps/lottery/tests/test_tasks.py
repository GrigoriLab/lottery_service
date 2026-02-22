from datetime import date, timedelta

import pytest

from apps.lottery.models import Ballot, Lottery, Winner
from apps.lottery.tasks import close_lottery


@pytest.mark.django_db
class TestCloseLotteryNoActive:
    def test_returns_empty_list_when_no_active_lotteries(self):
        result = close_lottery()
        assert result == []

    def test_ignores_draft_lotteries(self, draft_lottery):
        result = close_lottery()
        assert result == []
        draft_lottery.refresh_from_db()
        assert draft_lottery.status == Lottery.Status.DRAFT

    def test_ignores_finished_lotteries(self, finished_lottery):
        result = close_lottery()
        assert result == []
        finished_lottery.refresh_from_db()
        assert finished_lottery.status == Lottery.Status.FINISHED


@pytest.mark.django_db
class TestCloseLotteryWithBallots:
    def test_closes_active_lottery(self, active_lottery, ballot):
        result = close_lottery()
        assert result == [active_lottery.id]
        active_lottery.refresh_from_db()
        assert active_lottery.status == Lottery.Status.FINISHED

    def test_creates_winner(self, active_lottery, ballot):
        close_lottery()
        winner = Winner.objects.get(lottery=active_lottery)
        assert winner.ballot == ballot
        assert winner.participant == ballot.participant

    def test_winner_selected_from_multiple_ballots(self, active_lottery, user, second_user):
        Ballot.objects.create(lottery=active_lottery, participant=user)
        Ballot.objects.create(lottery=active_lottery, participant=second_user)

        close_lottery()

        winner = Winner.objects.get(lottery=active_lottery)
        assert winner.participant in [user, second_user]


@pytest.mark.django_db
class TestCloseLotteryWithoutBallots:
    def test_closes_lottery_without_ballots(self, active_lottery):
        result = close_lottery()
        assert result == [active_lottery.id]
        active_lottery.refresh_from_db()
        assert active_lottery.status == Lottery.Status.FINISHED

    def test_no_winner_created(self, active_lottery):
        close_lottery()
        assert not Winner.objects.filter(lottery=active_lottery).exists()


@pytest.mark.django_db
class TestCloseLotteryMultiple:
    def test_closes_all_active_lotteries(self, db):
        lottery1 = Lottery.objects.create(
            status=Lottery.Status.ACTIVE, expires_at=date.today() + timedelta(days=1)
        )
        lottery2 = Lottery.objects.create(
            status=Lottery.Status.ACTIVE, expires_at=date.today() + timedelta(days=2)
            # TODO: should we clause all lotteries or just expired ones?
        )

        result = close_lottery()

        assert set(result) == {lottery1.id, lottery2.id}
        lottery1.refresh_from_db()
        lottery2.refresh_from_db()
        assert lottery1.status == Lottery.Status.FINISHED
        assert lottery2.status == Lottery.Status.FINISHED

    def test_creates_winners_for_each_lottery_with_ballots(self, user, db):
        lottery1 = Lottery.objects.create(
            status=Lottery.Status.ACTIVE, expires_at=date.today() + timedelta(days=1)
        )
        lottery2 = Lottery.objects.create(
            status=Lottery.Status.ACTIVE, expires_at=date.today() + timedelta(days=2)
        )
        Ballot.objects.create(lottery=lottery1, participant=user)
        Ballot.objects.create(lottery=lottery2, participant=user)

        close_lottery()

        assert Winner.objects.count() == 2
        assert Winner.objects.filter(lottery=lottery1).exists()
        assert Winner.objects.filter(lottery=lottery2).exists()

    def test_mixed_lotteries_only_closes_active(self, user, db):
        active = Lottery.objects.create(
            status=Lottery.Status.ACTIVE, expires_at=date.today() + timedelta(days=1)
        )
        draft = Lottery.objects.create(
            status=Lottery.Status.DRAFT, expires_at=date.today() + timedelta(days=1)
        )
        finished = Lottery.objects.create(
            status=Lottery.Status.FINISHED, expires_at=date.today() - timedelta(days=1)
        )
        Ballot.objects.create(lottery=active, participant=user)

        result = close_lottery()

        assert result == [active.id]
        draft.refresh_from_db()
        finished.refresh_from_db()
        assert draft.status == Lottery.Status.DRAFT
        assert finished.status == Lottery.Status.FINISHED
        assert Winner.objects.count() == 1
