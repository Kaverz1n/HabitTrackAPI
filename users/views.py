from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    '''
    Создание пользователя сервиса
    '''
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            password = serializer.validated_data.pop('password')
            user = User.objects.create(**serializer.validated_data)
            user.set_password(password)
            user.save()

            return Response({'message': 'Пользователь успешно создан!'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
