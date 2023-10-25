from datetime import datetime
from celery import shared_task
from telegram_bot.services import BOT
from telegram_bot.models import TelegramUser


@shared_task
def start_bot() -> None:
    '''
    Задача запускает бота в нон-стоп режиме
    :return:
    '''
    BOT.polling(none_stop=True)


@shared_task
def send_reminders(*args) -> None:
    '''
    Задача отправляет напоминание пользователю о том,
    что настало время выполнять привычку
    :param args: данные о привычке
    :return:
    '''
    username, action, place, time, executed_time, is_positive, reward = [arg for arg in args]
    chat_id = TelegramUser.objects.get(username=username[1:])

    timee_to_execute = datetime.strptime(executed_time, "%H:%M:%S")
    start_time = datetime.strptime("00:00:00", "%H:%M:%S")
    seconds = round((timee_to_execute - start_time).total_seconds())

    if not is_positive:
        BOT.send_message(
            chat_id=chat_id,
            text=f'"Я буду {action} в {time[:5]} в {place}"\n\n'
                 f'Такое обещание вы себе дали! Время выполнять привычку!\n'
                 f'Время на выполнение: {seconds} секунд\n\n'
                 f'Награда: {reward}'
        )
    else:
        BOT.send_message(
            chat_id=chat_id,
            text=f'"Я буду {action} в {time[:5]} в {place}"\n\n'
                 f'Приятно слышать! Время приятной привычки!\n'
                 f'Время на выполнение: {seconds} секунд\n\n'
        )
