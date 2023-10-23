from rest_framework.exceptions import ValidationError


class TelegramNicknameValidator:
    '''
    Валидатор, отвечающий за проверку того,
    что пользователь указал верный никнейм
    '''

    def __init__(self, field) -> None:
        self.field = field

    def __call__(self, value) -> None:
        telegram_nickname = dict(value).get(self.field)

        if not telegram_nickname.startswith('@'):
            raise ValidationError("Телеграм-никнейм должен быть указан, начиная с символа '@'.")
