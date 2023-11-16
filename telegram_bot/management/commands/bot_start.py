from django.core.management.base import BaseCommand

from telegram_bot.services import BOT


class Command(BaseCommand):
    '''
    Команда для запуска телеграм бота
    '''

    def handle(self, *args, **options) -> None:
        BOT.polling(none_stop=True)
