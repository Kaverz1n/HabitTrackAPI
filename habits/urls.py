from habits.apps import HabitsConfig
from habits.views import HabitViewSet

from rest_framework.routers import DefaultRouter

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habits')

urlpatterns = [] + router.urls
