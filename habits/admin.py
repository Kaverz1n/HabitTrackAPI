from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'time', 'is_positive', 'is_public',)
    list_filter = ('user', 'is_positive', 'is_public',)
    search_fields = ('user', 'action',)
    ordering = ('pk',)
