from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    HabitRewardValidator, ExecutedTimeValidator, HabitIsPositiveValidator,
    IsPositiveValidator, PeriodicityValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для модели привычки
    '''

    class Meta:
        model = Habit
        fields = (
            'user',
            'place',
            'time',
            'action',
            'is_positive',
            'related_habit',
            'periodicity',
            'reward',
            'executed_time',
            'is_public',
        )
        validators = [
            HabitRewardValidator(fields=['related_habit', 'reward']),
            ExecutedTimeValidator(field='executed_time'),
            HabitIsPositiveValidator(field='related_habit'),
            IsPositiveValidator(fields=['is_positive', 'reward', 'related_habit']),
            PeriodicityValidator(field='periodicity')
        ]
