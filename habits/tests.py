from django.core.management import call_command

from habits.models import Habit

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User


class HabitTestCase(APITestCase):
    '''
    Тестирование модели Habit
    '''

    def setUp(self) -> None:
        call_command('flush', interactive=False)
        self.user = User.objects.create(telegram_nickname='@admin', password='admin', is_superuser=True)
        self.token = f'Bearer {AccessToken.for_user(self.user)}'
        self.habit = Habit.objects.create(
            user=self.user,
            place='test',
            time='02:02:02',
            action='test',
            is_positive=True,
            periodicity=1
        )

    def test_create_habit(self) -> None:
        '''
        Тестирование создания привычки
        '''
        data = {
            'place': 'test',
            'time': '01:01:01',
            'action': 'test',
            'is_positive': True,
            'periodicity': 1,
        }

        response = self.client.post(
            '/api/habits/',
            data=data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.json(),
            {
                'pk': 2,
                'user': 1,
                'place': 'test',
                'time': '01:01:01',
                'action': 'test',
                'is_positive': True,
                'related_habit': None,
                'periodicity': 1,
                'reward': None,
                'executed_time': '00:02:00'
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_validators(self) -> None:
        '''
        Тестирование валидаторов
        '''

        # тестирование HabitRewardValidator
        data = {
            'place': 'test',
            'time': '01:01:01',
            'action': 'test',
            'related_habit': 1,
            'reward': 'test'
        }

        response = self.client.post(
            '/api/habits/',
            data=data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.data,
            {
                'non_field_errors': ['Не может быть одновременный выбор связанной привычки и указания вознаграждения.']
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # тестирование ExecutedTimeValidator
        data = {
            'place': 'test',
            'time': '01:01:01',
            'action': 'test',
            'executed_time': '01:01:01'
        }

        response = self.client.post(
            '/api/habits/',
            data=data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.data,
            {
                'non_field_errors': ['Время выполнения привычки не может превышать 120 секунд.']
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # тестирование HabitIsPositiveValidator
        Habit.objects.create(
            user=self.user,
            place='test',
            time='01:01:01',
            action='test',
        )

        data = {
            'place': 'test',
            'time': '01:01:01',
            'action': 'test',
            'related_habit': 2,
        }

        response = self.client.post(
            '/api/habits/',
            data=data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.data,
            {
                'non_field_errors': [
                    'В связанные привычки могут попадать только привычки с признаком приятной привычки.'
                ]
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # тестирование IsPositiveValidator
        data = {
            'place': 'test',
            'time': '01:01:01',
            'action': 'test',
            'is_positive': True,
            'related_habit': 1,
        }

        response = self.client.post(
            '/api/habits/',
            data=data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.data,
            {
                'non_field_errors': [
                    'У приятной привычки не может быть вознаграждения или связанной привычки.'
                ]
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        data = {
            'place': 'test',
            'time': '01:01:01',
            'action': 'test',
            'is_positive': True,
            'reward': 'test'
        }

        response = self.client.post(
            '/api/habits/',
            data=data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.data,
            {
                'non_field_errors': [
                    'У приятной привычки не может быть вознаграждения или связанной привычки.'
                ]
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # тестирование PeriodicityValidator
        data = {
            'place': 'test',
            'time': '01:01:01',
            'action': 'test',
            'periodicity': 8
        }

        response = self.client.post(
            '/api/habits/',
            data=data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.data,
            {
                'non_field_errors': [
                    'Нельзя выполнять привычку реже, чем 1 раз в 7 дней.'
                ]
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_list_habit(self) -> None:
        '''
        Тестирование отображение списка привычек
        '''

        # Тестирование вывода не публичных привычек
        Habit.objects.create(
            user=self.user,
            place='test',
            time='01:01:01',
            action='test',
        )

        response = self.client.get(
            '/api/habits/',
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.json(),
            {
                'count': 0, 'next': None, 'previous': None, 'results': []
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # тестирование вывода публичных привычек
        Habit.objects.create(
            user=self.user,
            place='test',
            time='01:01:01',
            action='test',
            is_public=True
        )

        response = self.client.get(
            '/api/habits/',
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.json(),
            {
                'count': 1, 'next': None, 'previous': None, 'results':
                [
                    {
                        'pk': 3,
                        'user': 1,
                        'place': 'test',
                        'time': '01:01:01',
                        'action': 'test',
                        'is_positive': False,
                        'related_habit': None,
                        'periodicity': 1,
                        'reward': None,
                        'executed_time': '00:02:00'
                    }
                ]
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_user_list_habit(self) -> None:
        '''
        Тестирования вывода списка привычек пользователя
        '''
        Habit.objects.create(
            user=None,
            place='test',
            time='02:02:02',
            action='test',
            is_positive=True,
            periodicity=1
        )

        response = self.client.get(
            '/api/my-habits/',
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.json(),
            {
                'count': 1, 'next': None, 'previous': None, 'results':
                [
                    {
                        'pk': 1,
                        'place': 'test',
                        'time': '02:02:02',
                        'action': 'test',
                        'is_positive': True,
                        'related_habit': None,
                        'periodicity': 1,
                        'reward': None,
                        'executed_time': '00:02:00'
                    }
                ]
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        Habit.objects.create(
            user=self.user,
            place='test',
            time='02:02:02',
            action='test',
            is_positive=True,
            periodicity=1
        )

        response = self.client.get(
            '/api/my-habits/',
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.json(),
            {
                'count': 2, 'next': None, 'previous': None, 'results':
                [
                    {
                        'pk': 1,
                        'place': 'test',
                        'time': '02:02:02',
                        'action': 'test',
                        'is_positive': True,
                        'related_habit': None,
                        'periodicity': 1,
                        'reward': None,
                        'executed_time': '00:02:00'
                    },
                    {
                        'pk': 3,
                        'place': 'test',
                        'time': '02:02:02',
                        'action': 'test',
                        'is_positive': True,
                        'related_habit': None,
                        'periodicity': 1,
                        'reward': None,
                        'executed_time': '00:02:00'
                    }
                ]
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_retrieve_habit(self) -> None:
        '''
        Тестирование отображение одной привычки
        '''
        response = self.client.get(
            '/api/habits/1/',
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.json(),
            {
                'pk': 1,
                'place': 'test',
                'time': '02:02:02',
                'action': 'test',
                'is_positive': True,
                'related_habit': None,
                'periodicity': 1,
                'reward': None,
                'executed_time': '00:02:00'
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        data = {
            'place': 'test',
            'time': '01:01:01',
            'action': 'test',
            'periodicity': 7
        }

        self.client.post(
            '/api/habits/',
            data=data,
            HTTP_AUTHORIZATION=self.token
        )

        response = self.client.get(
            '/api/habits/2/',
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.json(),
            {
                'pk': 2,
                'place': 'test',
                'time': '01:01:01',
                'action': 'test',
                'is_positive': False,
                'related_habit': None,
                'periodicity': 7,
                'reward': None,
                'executed_time': '00:02:00'
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_habit(self) -> None:
        '''
        Тестирование обновления привычки
        '''

        # тестирование PUT
        data = {
            'pk': 1,
            'place': 'changed_field',
            'time': '02:02:02',
            'action': 'changed_field',
            'is_positive': True,
            'periodicity': 1,
            'executed_time': '00:02:00'
        }

        response = self.client.put(
            '/api/habits/1/',
            data=data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.json(),
            {
                'pk': 1,
                'place': 'changed_field',
                'time': '02:02:02',
                'action': 'changed_field',
                'is_positive': True,
                'related_habit': None,
                'periodicity': 1,
                'reward': None,
                'executed_time': '00:02:00'
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Тестирование PATCH
        response = self.client.patch(
            '/api/habits/1/',
            data=data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.json(),
            {
                'detail': 'Метод \"PATCH\" не разрешен.'
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_delete_habit(self) -> None:
        '''
        Тестирование удаления привычки
        '''
        response = self.client.delete(
            '/api/habits/1/',
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            list(Habit.objects.all()),
            []
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def tearDown(self) -> None:
        pass
