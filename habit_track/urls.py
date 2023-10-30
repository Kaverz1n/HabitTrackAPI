from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="HabitTrackAPI",
        default_version='v1',
        description="Simple API instructions ",
        terms_of_service="Test",
        contact=openapi.Contact(email="dima.captan@yandex.ru"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('habits.urls', namespace='habits')),
    path('api/', include('users.urls', namespace='users')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
