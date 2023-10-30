from django.core.management import call_command

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    '''
    Тестирование модели User
    '''

    def setUp(self) -> None:
        call_command('flush', interactive=False)

    def test_registration(self):
        '''
        Тестирование регистрации пользователей
        '''
        data = {
            'telegram_nickname': '@TEST',
            'password': 'TEST'
        }

        response = self.client.post(
            '/api/registration/',
            data=data
        )

        self.assertEqual(
            response.json(),
            {
                'message': 'Пользователь успешно создан!'
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            User.objects.all().first().telegram_nickname,
            '@TEST'
        )

    def test_validators(self):
        '''
        Тестирование валидаторов
        '''
        data = {
            'telegram_nickname': 'TEST',
            'password': 'TEST'
        }

        response = self.client.post(
            '/api/registration/',
            data=data
        )

        self.assertEqual(
            response.json(),
            {
                'non_field_errors': ["Телеграм-никнейм должен быть указан, начиная с символа '@'."]
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_authorization(self):
        '''
        Тестирование авторизации
        '''
        data = {
            'telegram_nickname': '@TEST',
            'password': 'TEST'
        }

        self.client.post(
            '/api/registration/',
            data=data
        )

        response = self.client.post(
            '/api/token/',
            data=data
        )

        response_keys = [key for key in response.json().keys()]

        self.assertEqual(
            response_keys[0],
            'refresh'
        )

        self.assertEqual(
            response_keys[1],
            'access'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def tearDown(self) -> None:
        pass
