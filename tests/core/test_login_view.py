import pytest
from django.urls import reverse
from rest_framework import status


"""
Тесты для LoginView:

Проверить, что при отправке POST-запроса с правильными данными аутентификация пользователя проходит успешно.
Проверить, что при отправке POST-запроса с неправильными данными возвращается ошибка аутентификации.
"""

@pytest.mark.django_db
class TestLoginView:
    # @pytest.mark.django_db
    def test_login_view_valid_credentials(self, client, user_factory):
        url = reverse('logged-in')
        # User.objects.create_user(username='testuser', password='TestPassword123')
        user = user_factory(username='testuser', password='CorrectPassword')
        data = {
            'username': 'testuser',
            'password': 'TestPassword123'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK


    # @pytest.mark.django_db
    def test_login_view_invalid_credentials(self, client, user_factory):
        # Создаем тестового пользователя с помощью user_factory
        user = user_factory(username='testuser', password='CorrectPassword')

        url = reverse('login_user')
        data = {
            'username': user.username,
            'password': 'IncorrectPassword'  # Неправильный пароль
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


