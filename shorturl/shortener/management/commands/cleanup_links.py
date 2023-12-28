from django.core.management.base import BaseCommand
from django.utils import timezone
from shortener.models import Link, DeletedCode

class Command(BaseCommand):
    help = 'Удаляет неиспользуемые ссылки и переносит их коды в DeletedCode'

    def add_arguments(self, parser):
        parser.add_argument('days', type=int, help='Количество дней неактивности для удаления ссылок')

    def handle(self, *args, **options):
        days = options['days']
        if days < 0:
            self.stdout.write(self.style.ERROR('Количество дней не должно быть отрицательным числом.'))
            return

        threshold_date = timezone.now() - timezone.timedelta(days=days)
        unused_links = Link.objects.filter(last_accessed__lte=threshold_date)

        for link in unused_links:
            DeletedCode.objects.create(code=link.short_url)
            link.delete()

        self.stdout.write(self.style.SUCCESS('Неиспользуемые ссылки были удалены и их коды будут переиспользованы'))
