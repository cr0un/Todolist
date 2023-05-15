import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestLoginView:
    def test_login_view_valid_credentials(self, client, user_factory):
        """
        Проверка авторизации
        """
        url = reverse('logged-in')
        user = user_factory(username='testuser', password='CorrectPassword')
        data = {
            'username': 'testuser',
            'password': 'TestPassword123'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_login_view_invalid_credentials(self, client, user_factory):
        """
        Проверка авторизации, если ошибка в пароле
        """
        # Создаем тестового пользователя с помощью user_factory
        user = user_factory(username='testuser', password='CorrectPassword')

        url = reverse('login_user')
        data = {
            'username': user.username,
            'password': 'IncorrectPassword'  # Неправильный пароль
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
