import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserRegistrationView:
    def test_user_registration_view_valid_data(self, client):
        """
        Проверка регистрация пользователя
        """
        url = reverse('signup')
        data = {
            'username': 'testuser',
            'password': 'TestPassword123',
            'password_repeat': 'TestPassword123',
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_user_registration_view_invalid_data(self, client):
        """
        Проверка ошибки регистрации при указании неверных данных
        """
        url = reverse('signup')
        data = {
            'username': 'testuser',
            'password': 'TestPassword123',
            'password_repeat': 'DifferentPassword123',  # неверный пароль
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

