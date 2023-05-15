import pytest
from django.urls import reverse
from rest_framework import status
from core.models import User


@pytest.mark.django_db
class TestUpdatePasswordView:
    def test_update_password_view_valid_data(self, client):
        """
        Проверка смены пароля
        """
        user = User.objects.create_user(username='testuser', password='TestPassword123')
        client.force_authenticate(user=user)

        url = reverse('update_password')
        data = {
            'old_password': 'TestPassword123',
            'new_password': 'NewPassword123'
        }
        response = client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_update_password_view_invalid_old_password(self, client, auth_client):
        """
        Проверка ошибки смены пароля, если указать неверно старый пароль
        """
        url = reverse('update_password')
        data = {
            'old_password': 'IncorrectPassword',  # Неправильный текущий пароль
            'new_password': 'NewPassword123'
        }
        response = auth_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_password_view_invalid_new_password(self, client, auth_client):
        """
        Проверка ошибки смены пароля, если указать неверно новый пароль (формат пароля не соблюден)
        """
        url = reverse('update_password')
        data = {
            'old_password': 'TestPassword123',
            'new_password': 'weak'  # Неправильный новый пароль
        }
        response = auth_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
