from datetime import timedelta, datetime

from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Habit(models.Model):
    '''
    Модель привычки пользователя
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', related_name='habit_user',
                             **NULLABLE)
    place = models.CharField(max_length=150, verbose_name='место', **NULLABLE)
    time = models.TimeField(verbose_name='время')
    action = models.CharField(max_length=150, verbose_name='действие')
    is_positive = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='связанная привычка', **NULLABLE)
    periodicity = models.PositiveSmallIntegerField(verbose_name='переодичность (в днях)', default=1)
    reward = models.TextField(verbose_name='вознаграждение', **NULLABLE)
    executed_time = models.TimeField(default="00:02:00", verbose_name='время на выполнение')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')

    def __str__(self) -> str:
        return f'Привычка {self.user.telegram_nickname} номер {self.pk}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
