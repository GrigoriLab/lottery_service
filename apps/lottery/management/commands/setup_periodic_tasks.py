from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Set up periodic tasks"

    def handle(self, *args, **options):
        crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
            hour=0,
        )

        task, task_created = PeriodicTask.objects.get_or_create(
            name="Close lottery",
            defaults={
                "crontab": crontab_schedule,
                "task": "apps.lottery.tasks.close_lottery",
            },
        )
        task.save()
