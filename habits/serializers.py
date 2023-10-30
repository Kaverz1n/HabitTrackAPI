from habits.models import Habit
from habits.validators import (
    HabitRewardValidator, ExecutedTimeValidator, HabitIsPositiveValidator,
    IsPositiveValidator, PeriodicityValidator
)

from rest_framework import serializers



class BaseHabitSerializer(serializers.ModelSerializer):
    '''
    Базовый сериализатор привычки
    '''

    class Meta:
        model = Habit
        fields = (
            'pk',
            'user',
            'place',
            'time',
            'action',
            'is_positive',
            'related_habit',
            'periodicity',
            'reward',
            'executed_time',
        )
        validators = [
            HabitRewardValidator(fields=['related_habit', 'reward']),
            ExecutedTimeValidator(field='executed_time'),
            HabitIsPositiveValidator(field='related_habit'),
            IsPositiveValidator(fields=['is_positive', 'reward', 'related_habit']),
            PeriodicityValidator(field='periodicity'),
        ]

    def create(self, validated_data) -> Habit:
        user = self.context['request'].user
        habit = Habit.objects.create(**validated_data, user=user)

        return habit


class HabitSerializer(BaseHabitSerializer):
    '''
    Сериализатор для модели привычки
    '''


class UserHabitSerializer(BaseHabitSerializer):
    '''
    Сериализатор для модели привычки текущего пользователя
    '''

    class Meta:
        model = Habit
        fields = (
            'pk',
            'place',
            'time',
            'action',
            'is_positive',
            'related_habit',
            'periodicity',
            'reward',
            'executed_time',
        )
        validators = BaseHabitSerializer.Meta.validators + []
