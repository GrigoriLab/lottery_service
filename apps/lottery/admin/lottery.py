from django.contrib import admin

from apps.lottery.models import Lottery


@admin.register(Lottery)
class LotteryAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "created_at", "expires_at")
    list_filter = ("status",)
