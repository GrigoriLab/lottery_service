from django.contrib import admin

from apps.lottery.models import Winner


@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ("id", "lottery", "participant", "selected_at")
