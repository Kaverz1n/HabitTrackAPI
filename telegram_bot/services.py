import telebot

from django.db import IntegrityError

from habit_track import settings

from telegram_bot.models import TelegramUser

TELEGRAM_TOKEN = settings.TELEGRAM_SECRET_KEY
BOT = telebot.TeleBot(TELEGRAM_TOKEN)


@BOT.message_handler(commands=['start'])
def handle_start(message) -> None:
    '''
    Функция, регистрирующая пользователей телеграм для
    включения напоминания о привычках
    :param message: сообщение пользователя
    '''
    user = message.from_user
    chat_id = user.id
    username = user.username

    try:
        TelegramUser.objects.create(username=username, chat_id=chat_id)
        BOT.send_message(
            chat_id=chat_id,
            text='Вы успешно записаны!'
        )
    except IntegrityError:
        BOT.send_message(
            chat_id=chat_id,
            text='Вы уже записаны!'
        )
