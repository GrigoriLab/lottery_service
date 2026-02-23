from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.lottery.models import Lottery


class Command(BaseCommand):
    help = "Create a new active lottery"

    def add_arguments(self, parser):
        parser.add_argument(
            "--hours",
            type=int,
            default=24,
            help="Hours until the lottery expires (default: 24)",
        )

    def handle(self, *args, **options):
        hours = options["hours"]
        lottery = Lottery.objects.create(
            status=Lottery.Status.ACTIVE,
            expires_at=timezone.now() + timedelta(hours=hours),
        )
        self.stdout.write(self.style.SUCCESS(f"Created {lottery} (expires in {hours}h)"))
