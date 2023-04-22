from django.core.management.base import BaseCommand, CommandError
from apps.tasks_pipeline.models import Monitoring


class Command(BaseCommand):
    help = 'Clean all Monitoring history'

    def handle(self, *args, **options):
        try:
            Monitoring.objects.all().delete()
        except Exception as exc:
            raise CommandError('Error on clean Monitoring history') from exc
        else:
            self.stdout.write(self.style.SUCCESS('Successfully clean'))
