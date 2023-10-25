from django.db import models


class TelegramUser(models.Model):
    '''
    Модель телеграм пользователя
    '''
    username = models.CharField(max_length=100, verbose_name='telegram-никнейм', unique=True)
    chat_id = models.PositiveIntegerField(verbose_name='чат-id', unique=True)

    def __str__(self) -> str:
        return f'{self.chat_id}'

    class Meta:
        verbose_name = 'телеграм пользователь'
        verbose_name_plural = 'телеграм пользователи'
