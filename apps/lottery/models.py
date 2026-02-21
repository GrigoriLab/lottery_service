from django.conf import settings
from django.db import models


class Lottery(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        FINISHED = "finished", "Finished"

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "lotteries"


class Ballot(models.Model):
    lottery = models.ForeignKey("lottery.Lottery", on_delete=models.CASCADE, related_name="ballots")
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ballots")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]


class Winner(models.Model):
    lottery = models.OneToOneField(Lottery, on_delete=models.CASCADE, related_name="winner")
    ballot = models.OneToOneField(Ballot, on_delete=models.CASCADE, related_name="winning_ballot")
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wins")
    selected_at = models.DateTimeField(auto_now_add=True)
