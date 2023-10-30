from rest_framework.serializers import ModelSerializer

from users.models import User
from users.validators import TelegramNicknameValidator


class UserSerializer(ModelSerializer):
    '''
    Сериализатор для модели пользователя
    '''

    class Meta:
        model = User
        fields = (
            'telegram_nickname',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}
        validators = [
            TelegramNicknameValidator(field='telegram_nickname')
        ]
