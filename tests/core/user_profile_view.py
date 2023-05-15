import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserProfileView:
    def test_user_profile_view_get_authenticated(self, client, auth_client):
        """
        Проверка получения профиля для авторизованного юзера
        """
        url = reverse('profile')
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_user_profile_view_get_unauthenticated(self, client):
        """
        Если пользователь не авторизован, то ошибка получения профиля
        """
        url = reverse('profile')
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_profile_view_update_authenticated(self, client, auth_client):
        """
        Проверка обновления профиля
        """
        url = reverse('profile')
        data = {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User'
        }
        response = auth_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
