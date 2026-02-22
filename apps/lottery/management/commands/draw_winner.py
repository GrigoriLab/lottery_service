from django.core.management.base import BaseCommand

from apps.lottery.tasks import close_lottery


class Command(BaseCommand):
    help = "Close all active lotteries and draw winners"

    def handle(self, *args, **options):
        closed_ids = close_lottery()
        if closed_ids:
            self.stdout.write(self.style.SUCCESS(f"Closed lotteries: {closed_ids}"))
        else:
            self.stdout.write("No active lotteries to close")
