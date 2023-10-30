from django.contrib import admin

from telegram_bot.models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'chat_id',)
    search_fields = ('username',)
    ordering = ('pk',)
