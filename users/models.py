from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''
    Модель пользователя сервиса
    '''
    username = None
    telegram_nickname = models.CharField(max_length=32, unique=True, verbose_name='telegram nickname')

    USERNAME_FIELD = "telegram_nickname"
    REQUIRED_FIELDS = []
