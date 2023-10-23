from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    '''
    Команда для создания администратора
    '''

    def handle(self, *args, **options) -> None:
        try:
            admin = User.objects.create(
                telegram_nickname='@admin',
                is_staff=True,
                is_superuser=True,
            )

            admin.set_password('admin')
            admin.save()

            self.stdout.write('Администратор успешно создан!')
        except Exception as e:
            self.stderr.write(f'Ошибка создания супервользователя!\nОшибка: {e}')
