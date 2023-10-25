import json
from datetime import time, datetime, timedelta

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from habits.models import Habit


def get_habit_datetime(habit_time: time) -> datetime:
    '''
    Возвращает время выполнения привычки в формате datetime
    :param habit_time: время выполнения привычки
    :return: datetime
    '''
    now = datetime.now()
    fulltime = datetime.combine(now, habit_time)

    if fulltime < now:
        fulltime += timedelta(days=1)

    return fulltime


def add_periodic_task(habit: Habit) -> None:
    '''
    Создание отложенной задачи на отправку
    напоминания о выполнении привычки
    :habit: привычка
    '''
    fulltime = get_habit_datetime(habit.time)

    schedule, created = IntervalSchedule.objects.get_or_create(
        every=habit.periodicity,
        period=IntervalSchedule.DAYS,
    )

    PeriodicTask.objects.create(
        interval=schedule,
        name=f'{habit.user.telegram_nickname} habit_{habit.pk}',
        task='telegram_bot.tasks.send_reminders',
        args=json.dumps(
            [
                habit.user.telegram_nickname,
                habit.action,
                habit.place,
                str(habit.time),
                str(habit.executed_time),
                habit.is_positive,
                habit.reward
            ],
            ensure_ascii=False
        ),
        start_time=fulltime
    )
