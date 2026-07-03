# parser/management/commands/run_crawler.py

from django.core.management.base import BaseCommand
from parser.Crawler import Crawler

class Command(BaseCommand):
    help = 'Запуск парсера в обычном синхронном режиме'

    def handle(self, *args, **options):
        self.stdout.write('Запуск краулера вручную...')
        Crawler()
        self.stdout.write(self.style.SUCCESS('Краулер завершил работу.'))