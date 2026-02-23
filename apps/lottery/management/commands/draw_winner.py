from django.core.management.base import BaseCommand

from apps.lottery.models import Winner
from apps.lottery.tasks import close_lottery


class Command(BaseCommand):
    help = "Close all active lotteries and draw winners"

    def handle(self, *args, **options):
        closed_ids = close_lottery()
        if not closed_ids:
            self.stdout.write("No active lotteries to close")
            return

        for lottery_id in closed_ids:
            try:
                winner = Winner.objects.get(lottery_id=lottery_id)
                self.stdout.write(self.style.SUCCESS(f"Lottery {lottery_id}: winner is {winner.participant.username}"))
            except Winner.DoesNotExist:
                self.stdout.write(f"Lottery {lottery_id}: no ballots, no winner")
