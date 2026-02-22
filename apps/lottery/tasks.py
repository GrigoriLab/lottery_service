import logging

from config import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def close_lottery(**kwargs):
    from .models import Ballot, Lottery, Winner

    active_lotteries = Lottery.objects.filter(status=Lottery.Status.ACTIVE)
    if not active_lotteries.exists():
        logger.info("No active lottery")

    closed_ids = []

    for lottery in active_lotteries:
        winning_ballot = Ballot.objects.filter(lottery=lottery).order_by("?").first()

        lottery.status = Lottery.Status.FINISHED
        lottery.save(update_fields=["status"])

        if winning_ballot:
            winner = Winner.objects.create(
                lottery=lottery,
                ballot=winning_ballot,
                participant=winning_ballot.participant,
            )
            logger.info(f"Winner is {winner.participant}")
        else:
            logger.info(f"No ballots submitted for lottery {lottery}")

        closed_ids.append(lottery.id)

    return closed_ids
