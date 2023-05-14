import pytest
from django.urls import reverse
from rest_framework import status

from core.models import User

"""
Тесты для UpdatePasswordView:

Проверить, что при отправке PUT-запроса с правильными данными происходит успешное обновление пароля пользователя.
Проверить, что при отправке PUT-запроса с неправильным текущим паролем возвращается ошибка.
Проверить, что при отправке PUT-запроса с неправильным новым паролем возвращается ошибка.
"""

@pytest.mark.django_db
class TestUpdatePasswordView:
    # @pytest.mark.django_db
    def test_update_password_view_valid_data(self, client):
        user = User.objects.create_user(username='testuser', password='TestPassword123')
        client.force_authenticate(user=user)

        url = reverse('update_password')
        data = {
            'old_password': 'TestPassword123',
            'new_password': 'NewPassword123'
        }
        response = client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK

    # @pytest.mark.django_db
    def test_update_password_view_invalid_old_password(self, client, auth_client):
        url = reverse('update_password')
        data = {
            'old_password': 'IncorrectPassword',  # Неправильный текущий пароль
            'new_password': 'NewPassword123'
        }
        response = auth_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # @pytest.mark.django_db
    def test_update_password_view_invalid_new_password(self, client, auth_client):
        url = reverse('update_password')
        data = {
            'old_password': 'TestPassword123',
            'new_password': 'weak'  # Неправильный новый пароль
        }
        response = auth_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
