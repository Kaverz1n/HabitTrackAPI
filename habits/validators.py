from datetime import timedelta

from rest_framework.serializers import ValidationError

from habits.models import Habit


class HabitRewardValidator:
    '''
    Валидатор, отвечающий за проверку того,
    что не может быть одновременный выбор связанной
    привычки и указания вознаграждения.
    '''

    def __init__(self, fields) -> None:
        self.fields = fields

    def __call__(self, value) -> None:
        fields = [dict(value).get(field) for field in self.fields]

        if not None in fields:
            raise ValidationError(
                'Не может быть одновременный выбор связанной привычки и указания вознаграждения.'
            )


class ExecutedTimeValidator:
    '''
    Валидатор, отвечающий за проверку того,
    что время выполнения привычки не может
    превышать 120 сек
    '''

    def __init__(self, field) -> None:
        self.field = field

    def __call__(self, value) -> None:
        try:
            max_time = 120
            executed_time = dict(value).get(self.field)
            executed_timedelta = timedelta(
                hours=executed_time.hour,
                minutes=executed_time.minute,
                seconds=executed_time.second
            )

            if int(executed_timedelta.total_seconds()) > max_time:
                raise ValidationError(
                    'Время выполнения привычки не может превышать 120 секунд.'
                )
        except AttributeError:
            pass


class HabitIsPositiveValidator:
    '''
    Валидтор, отвечающий за проверку того,
    что в связанные привычки могут попадать
    только привычки с признаком приятной привычки.
    '''

    def __init__(self, field) -> None:
        self.field = field

    def __call__(self, value):
        related_habit = dict(value).get(self.field)

        if related_habit is not None:
            related_habit = Habit.objects.get(pk=related_habit.pk)

            if not related_habit.is_positive:
                raise ValidationError(
                    'В связанные привычки могут попадать только привычки с признаком приятной привычки.'
                )


class IsPositiveValidator:
    '''
    Валидатор, отвечающий за проверку того,
    что у приятной привычки не может быть
    вознаграждения или связанной привычки.
    '''

    def __init__(self, fields) -> None:
        self.fields = fields

    def __call__(self, value):
        fields = [dict(value).get(field) for field in self.fields]
        is_positive, reward, related_habit = [field for field in fields]

        if not is_positive:
            return

        if related_habit is not None or reward is not None:
            raise ValidationError(
                'У приятной привычки не может быть вознаграждения или связанной привычки.'
            )


class PeriodicityValidator:
    '''
    Валидатор, отвечающий за проверку того,
    что нельзя выполнять привычку реже,
    чем 1 раз в 7 дней.
    '''

    def __init__(self, field) -> None:
        self.field = field

    def __call__(self, value) -> None:
        try:
            periodicity = dict(value).get(self.field)

            if periodicity > 7:
                raise ValidationError(
                    'Нельзя выполнять привычку реже, чем 1 раз в 7 дней.'
                )
        except TypeError:
            pass
