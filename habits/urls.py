from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitViewSet, UserHabitListAPIView

from rest_framework.routers import DefaultRouter

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habits')

urlpatterns = [
    path('my-habits/', UserHabitListAPIView.as_view(), name='user_habits_list'),
] + router.urls
