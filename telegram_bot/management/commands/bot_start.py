from django.core.management.base import BaseCommand
from telegram_bot.tasks import start_bot


class Command(BaseCommand):
    '''
    Команда для запуска телеграм бота
    '''

    def handle(self, *args, **options) -> None:
        start_bot.delay()
