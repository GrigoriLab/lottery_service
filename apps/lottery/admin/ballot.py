from django.contrib import admin

from apps.lottery.models import Ballot


@admin.register(Ballot)
class BallotAdmin(admin.ModelAdmin):
    list_display = ("id", "lottery", "participant", "submitted_at")
    list_filter = ("lottery",)
