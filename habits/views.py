from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics

from habits.models import Habit
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer, UserHabitSerializer
from habits.services import add_periodic_task
from habits.paginators import HabitPaginator, UserHabitPaginator


class HabitViewSet(viewsets.ModelViewSet):
    '''
    ViewSet для модели Habit
    '''
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        if self.action == 'list':
            return Habit.objects.filter(is_public=True).order_by('-time')

        return Habit.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'create'):
            return HabitSerializer

        return UserHabitSerializer

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        habit = serializer.instance
        add_periodic_task(habit)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            return Response({"detail": "Метод \"PATCH\" не разрешен."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        super().update(request, *args, **kwargs)


class UserHabitListAPIView(generics.ListAPIView):
    '''
    Список привычек пользователя
    '''
    serializer_class = UserHabitSerializer
    pagination_class = UserHabitPaginator

    def get_queryset(self):
        user = self.request.user

        return Habit.objects.filter(user=user)
