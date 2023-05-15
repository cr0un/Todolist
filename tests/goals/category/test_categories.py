import pytest
from django.urls import reverse
from rest_framework import status
from goals.models import GoalCategory
from tests.factories import GoalCategoryFactory, UserFactory
from tests.goals.test_utils import create_board_and_category, add_participant_to_board


@pytest.mark.django_db
class TestCategoriesView:
    def test_create_goal_category_success(self, client, user):
        """
        Проверка успешного создания категории
        """
        client.force_authenticate(user=user)
        board, category = create_board_and_category(client, user)

        assert category is not None
        assert GoalCategory.objects.filter(title="Test Category", board=board).exists()

    def test_retrieve_goal_category_success(self, client, user):
        """
        Проверка успешного получения категории
        """
        client.force_authenticate(user=user)
        board, category = create_board_and_category(client, user)
        url = reverse("goals:retrieve_update_destroy_goal_category", args=[category.id])
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == category.id

    def test_delete_goal_category_success(self, client, user):
        """
        Проверка успешного удаления категории
        """
        client.force_authenticate(user=user)

        # Создание доски и категории с использованием вспомогательной функции
        board, category = create_board_and_category(client, user)

        # Тестирование успешного удаления категории
        url = reverse("goals:retrieve_update_destroy_goal_category", args=[category.id])
        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not GoalCategory.objects.exclude(id=category.id).exists()

    def test_update_goal_category_success(self, client, user):
        """
        Проверка успешного обновления категории
        """
        client.force_authenticate(user=user)

        # Создание доски и категории с использованием вспомогательной функции
        board, category = create_board_and_category(client, user)

        new_title = "Updated Category"
        payload = {
            "title": new_title,
        }
        url = reverse("goals:retrieve_update_destroy_goal_category", args=[category.id])
        response = client.patch(url, data=payload)  # Передаем данные в метод patch

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == new_title
        assert GoalCategory.objects.get(id=category.id).title == new_title

    def test_retrieve_goal_category_permission_denied(self, client, user):
        """
        Проверка отказа в получении категории, если это не владелец категории
        """
        client.force_authenticate(user=user)
        category = GoalCategoryFactory()

        # Создаем другого пользователя без доступа к категории
        other_user = UserFactory()

        # Имитируем аутентификацию другого пользователя
        client.force_authenticate(user=other_user)

        # Попытка получения категории
        url = reverse("goals:retrieve_update_destroy_goal_category", args=[category.id])
        response = client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "Not found."

    def test_update_goal_category_writter_denied(self, client, user):
        """
        Юзер с ролью "читатель" не может редактировать категорию
        """
        client.force_authenticate(user=user)

        # Создание доски и категории с использованием вспомогательной функции
        board, category = create_board_and_category(client, user)

        # Создаем другого пользователя без доступа к категории
        other_user = UserFactory()

        # Добавляем этого пользователя в доску с ролью "читатель" (3)
        add_participant_to_board(board, other_user, 3)

        # Имитируем аутентификацию другого пользователя
        client.force_authenticate(user=other_user)

        new_title = "Updated Category"
        payload = {
            "title": new_title,
        }

        url = reverse("goals:retrieve_update_destroy_goal_category", args=[category.id])
        response = client.patch(url, data=payload)  # Передаем данные в метод patch

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert GoalCategory.objects.get(id=category.id).title != new_title

    def test_update_goal_category_editor_success(self, client):
        """
        Юзер с ролью "редактор" может редактировать категорию
        """
        # Создаем двух пользователей
        user1 = UserFactory()
        user2 = UserFactory()

        # Аутентифицируем первого пользователя
        client.force_authenticate(user=user1)

        # Создаем доску и категорию с первым пользователем
        board, category = create_board_and_category(client, user1)

        # Добавляем второго пользователя на доску с ролью редактора (2)
        add_participant_to_board(board, user2, 2)

        # Аутентифицируем второго пользователя
        client.force_authenticate(user=user2)

        # Обновляем категорию
        new_title = "Updated Category"
        payload = {
            "title": new_title,
        }
        url = reverse("goals:retrieve_update_destroy_goal_category", args=[category.id])
        response = client.patch(url, data=payload)

        # Проверяем успешное обновление категории
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == new_title
        assert GoalCategory.objects.get(id=category.id).title == new_title
