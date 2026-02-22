from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Set up periodic tasks"

    def add_arguments(self, parser):
        parser.add_argument(
            "--test",
            action="store_true",
            dest="is_test",
            default=False,
            help="Create lottery and set up periodic task for 10 seconds",
        )

    def handle(self, *args, **options):
        crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
            hour=0,
        )

        task, task_created = PeriodicTask.objects.get_or_create(
            name="Close lottery and pick winner",
            defaults={
                "crontab": crontab_schedule,
                "task": "apps.lottery.tasks.close_lottery",
            },
        )
        if options["is_test"]:
            test_schedule, _ = IntervalSchedule.objects.get_or_create(
                every=30,
                period=IntervalSchedule.SECONDS,
            )
            task.interval = test_schedule
            task.crontab = None
        else:
            task.interval = None
            task.crontab = crontab_schedule
        task.save()
