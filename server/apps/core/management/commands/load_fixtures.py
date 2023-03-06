"""Модуль с командой для применения фикстур."""
import time
from os import listdir
from os.path import exists, join

from django.core.management import call_command
from django.core.management.base import BaseCommand

from devind.settings import BASE_DIR


class Command(BaseCommand):
    """Команда применения фикстур проекта."""

    helps = 'Первоначальное развертывание проекта.'
    fixtures_path = join(BASE_DIR, 'apps', '%s', 'fixtures')
    dir_apps = join(BASE_DIR, 'apps')

    def add_arguments(self, parser) -> None:
        """Аргументы команды."""
        parser.add_argument(
            '--app',
            default='core',
            help='Указываем приложение для парсинга'
        )

    def app_fixtures(self, app: str, fixture_location: str) -> None:
        """Применение фикстуры."""
        if exists(fixture_location):
            self.stdout.write(f'  Приложение {app}:')
            for fixture in sorted(listdir(fixture_location)):
                self.stdout.write(f'    Модель {fixture[4:-5]}')
                call_command('loaddata', fixture)
        else:
            self.stdout.write(f'В приложении отсутствуют фикстуры {app}.')

    def handle(self, *args, **options) -> None:
        """Описание команды."""
        start_time = time.time()
        self.stdout.write('Инициализация проекта:')
        if options['app']:
            self.app_fixtures(app=options['app'], fixture_location=self.fixtures_path % options['app'])
        else:
            for app in sorted(listdir(self.dir_apps)):
                self.app_fixtures(app=app, fixture_location=self.fixtures_path % app)
        self.stdout.write(f'Развертывание проекта завершено за время: {str((time.time() - start_time) / 60)} минут')
