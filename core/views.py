from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  permissions
from django.contrib.auth import authenticate, login, get_user_model
from rest_framework import generics
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import User
from .serializers import UserRegistrationSerializer, UserSerializer, PasswordSerializer


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = []
    authentication_classes = []
    serializer_class = UserRegistrationSerializer


class LoginView(APIView):
    def post(self, request):
        # Получение данных из тела запроса
        username = request.data.get('username')
        password = request.data.get('password')

        # Аутентификация пользователя
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Успешная аутентификация и вход
            login(request, user)
            # Возвращаем данные пользователя в ответе
            response_data = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # Неуспешная аутентификация
            response_data = {'error': 'Invalid username or password'}
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordView(generics.UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = PasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"success": "Password updated successfully"}, status=status.HTTP_200_OK)


def logged_in(request):
    return HttpResponse('Успешный вход через VK')

def login_error(request):
    return HttpResponse('Ошибка входа через VK')






