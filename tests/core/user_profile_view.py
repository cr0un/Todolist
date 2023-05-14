import pytest
from django.urls import reverse
from rest_framework import status


"""
Тесты для UserProfileView:

Проверить, что при запросе GET-запроса для авторизованного пользователя возвращается его профиль.
Проверить, что при запросе PUT-запроса для авторизованного пользователя происходит успешное обновление профиля.
Проверить, что при запросе DELETE-запроса для авторизованного пользователя происходит успешное удаление профиля.
"""

@pytest.mark.django_db
class TestUserProfileView:
    # @pytest.mark.django_db
    def test_user_profile_view_get_authenticated(self, client, auth_client):
        url = reverse('profile')
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    # @pytest.mark.django_db
    def test_user_profile_view_get_unauthenticated(self, client):
        url = reverse('profile')
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # @pytest.mark.django_db
    def test_user_profile_view_update_authenticated(self, client, auth_client):
        url = reverse('profile')
        data = {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User'
        }
        response = auth_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK

    # @pytest.mark.django_db
    def test_user_profile_view_delete_authenticated(self, client, auth_client):
        url = reverse('profile')
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
