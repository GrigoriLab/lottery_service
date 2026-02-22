from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.lottery.models import Ballot, Lottery, Winner

User = get_user_model()

SUPERUSER_USERNAME = "admin"
SUPERUSER_EMAIL = "admin@lottery.local"
SUPERUSER_PASSWORD = "admin"

PARTICIPANTS = [
    {"username": "alice", "email": "alice@example.com", "password": "password123"},
    {"username": "bob", "email": "bob@example.com", "password": "password123"},
    {"username": "charlie", "email": "charlie@example.com", "password": "password123"},
]


class Command(BaseCommand):
    help = "Create test data"

    def handle(self, *args, **options):
        if User.objects.filter(username=SUPERUSER_USERNAME).exists():
            self.stdout.write(f"Superuser '{SUPERUSER_USERNAME}' already exists, skipping")
        else:
            User.objects.create_superuser(
                username=SUPERUSER_USERNAME,
                email=SUPERUSER_EMAIL,
                password=SUPERUSER_PASSWORD,
            )
            msg = f"Created superuser '{SUPERUSER_USERNAME}' (password: {SUPERUSER_PASSWORD})"
            self.stdout.write(self.style.SUCCESS(msg))

        users = []
        for data in PARTICIPANTS:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={"email": data["email"]},
            )
            if created:
                user.set_password(data["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user '{user.username}'"))
            else:
                self.stdout.write(f"User '{user.username}' already exists, skipping")
            users.append(user)

        now = timezone.now()
        alice, bob, charlie = users

        finished_lottery = Lottery.objects.create(status=Lottery.Status.FINISHED, expires_at=now - timedelta(days=1))
        b1 = Ballot.objects.create(lottery=finished_lottery, participant=alice)
        Ballot.objects.create(lottery=finished_lottery, participant=bob)
        Winner.objects.create(lottery=finished_lottery, ballot=b1, participant=alice)
        self.stdout.write(self.style.SUCCESS("Created finished lottery (winner: alice)"))

        active_lottery = Lottery.objects.create(status=Lottery.Status.ACTIVE, expires_at=now + timedelta(hours=1))
        Ballot.objects.create(lottery=active_lottery, participant=bob)
        Ballot.objects.create(lottery=active_lottery, participant=charlie)
        Ballot.objects.create(lottery=active_lottery, participant=alice)
        self.stdout.write(self.style.SUCCESS("Created active lottery with 3 ballots"))

        Lottery.objects.create(status=Lottery.Status.DRAFT, expires_at=now + timedelta(days=7))
        self.stdout.write(self.style.SUCCESS("Created draft lottery"))

        self.stdout.write(self.style.SUCCESS("\nDone! Test data summary:"))
        self.stdout.write(f"Superuser: {SUPERUSER_USERNAME} / {SUPERUSER_PASSWORD}")
        self.stdout.write("Participants: alice, bob, charlie (password: password123)")
        self.stdout.write("Lottery #1: finished (winner: alice)")
        self.stdout.write("Lottery #2: active (ballots from bob, charlie, alice)")
        self.stdout.write("Lottery #3: draft (no ballots)")
