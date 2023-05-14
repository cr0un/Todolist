import pytest
from django.urls import reverse
from rest_framework import status


"""
Тесты для UserRegistrationView:

Проверить, что при отправке POST-запроса с правильными данными происходит успешная регистрация пользователя.
Проверить, что при отправке POST-запроса с неправильными данными (несовпадение паролей) возвращается ошибка.
"""


@pytest.mark.django_db
class TestUserRegistrationView:
    def test_user_registration_view_valid_data(self, client):
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
        url = reverse('signup')
        data = {
            'username': 'testuser',
            'password': 'TestPassword123',
            'password_repeat': 'DifferentPassword123',  # Incorrect password repeat
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
