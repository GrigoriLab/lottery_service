from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.lottery.models import Ballot, Lottery

User = get_user_model()


class Command(BaseCommand):
    help = "Submit a ballot for a user in an active lottery"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="Username of the participant")
        parser.add_argument("lottery_id", type=int, help="ID of the lottery")

    def handle(self, *args, **options):
        username = options["username"]
        lottery_id = options["lottery_id"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f"User '{username}' not found")

        try:
            lottery = Lottery.objects.get(id=lottery_id)
        except Lottery.DoesNotExist:
            raise CommandError(f"Lottery {lottery_id} not found")

        if lottery.status != Lottery.Status.ACTIVE:
            raise CommandError(f"Lottery {lottery_id} is not active (status: {lottery.status})")

        ballot = Ballot.objects.create(lottery=lottery, participant=user)
        self.stdout.write(self.style.SUCCESS(f"Created {ballot}"))
