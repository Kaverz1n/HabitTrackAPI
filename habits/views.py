from rest_framework import viewsets

from habits.models import Habit
from habits.serializers import HabitSerializer
from habits.paginators import HabitPaginator


class HabitViewSet(viewsets.ModelViewSet):
    '''
    ViewSet для модели Habit
    '''
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
