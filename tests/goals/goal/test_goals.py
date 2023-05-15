import pytest
from rest_framework.reverse import reverse
from rest_framework import status
from goals.models import Goal
from tests.factories import UserFactory, GoalFactory
from tests.goals.test_utils import create_board_and_category, add_participant_to_board


@pytest.mark.django_db
class TestGoalsView:
    def test_create_goal_success(self, auth_client):
        """
        Проверка создания цели
        """
        # Создание пользователя и доски с категорией
        user = UserFactory()
        board, category = create_board_and_category(auth_client, user)

        # Подготовка данных для создания цели
        url = reverse('goals:goal_create')
        payload = {
            'title': 'Test Goal',
            'description': 'Test Description',
            'category': category.id,
        }

        # Отправка запроса на создание цели
        response = auth_client.post(url, data=payload)

        # Проверка статуса ответа и наличия созданной цели в базе данных
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data

        # Проверка, что цель была создана с правильными значениями полей
        goal_id = response.data['id']
        goal = Goal.objects.get(id=goal_id)
        assert goal.title == payload['title']
        assert goal.description == payload['description']
        assert goal.category_id == category.id
        assert goal.user_id == user.id

    def test_update_goal_success(self, auth_client):
        """
        Проверка обновления цели
        """
        # Создание пользователя, доски, категории и цели
        user = UserFactory()
        board, category = create_board_and_category(auth_client, user)
        goal = GoalFactory(category=category, user=user)

        # Подготовка данных для обновления цели
        url = reverse('goals:goal_view', args=[goal.id])
        payload = {
            'title': 'Updated Goal Title',
        }

        # Отправка запроса на обновление цели
        response = auth_client.patch(url, data=payload)

        # Проверка статуса ответа и получение обновленной цели из базы данных
        assert response.status_code == status.HTTP_200_OK
        goal.refresh_from_db()

        # Проверка, что цель была обновлена с правильными значениями полей
        assert goal.title == payload['title']

    def test_delete_goal_success(self, auth_client):
        """
        Проверка удаления цели
        is_deleted становится True, пользователь не видит цель после ее удаления
        """
        # Создание пользователя, доски, категории и цели
        user = UserFactory()
        board, category = create_board_and_category(auth_client, user)
        goal = GoalFactory(category=category, user=user)

        # Подготовка данных для удаления цели
        url = reverse('goals:goal_view', args=[goal.id])

        # Отправка запроса на удаление цели
        response = auth_client.delete(url)

        # Проверка статуса ответа и проверка, что цель была удалена
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Обновление объекта цели из базы данных
        goal.refresh_from_db()

        # Проверка, что параметр is_deleted у цели установлен на True
        assert goal.is_deleted

        # Проверка, что при попытке получить цель по её ID возвращается ошибка "Not found" и код ответа 404
        url_get = reverse('goals:goal_view', args=[goal.id])
        response_get = auth_client.get(url_get)
        assert response_get.status_code == status.HTTP_404_NOT_FOUND
        assert response_get.data == {'detail': 'Not found.'}

    def test_update_goal_permission_denied(self, auth_client):
        """
        Юзер с ролью "читатель" не может редактировать цель
        """
        # Создание пользователей, доски, категории и цели
        user_1 = UserFactory()
        board, category = create_board_and_category(auth_client, user_1)
        goal = GoalFactory(category=category, user=user_1)

        # Создание второго пользователя
        user_2 = UserFactory()

        # Добавление второго пользователя в доску с ролью "читатель" (3)
        add_participant_to_board(board, user_2, 3)

        # Подготовка данных для обновления цели
        url = reverse('goals:goal_view', args=[goal.id])
        new_title = "Updated Goal"
        payload = {
            "title": new_title,
        }

        # Аутентификация второго пользователя
        auth_client.force_authenticate(user=user_2)

        # Отправка запроса на обновление цели
        response = auth_client.patch(url, data=payload)

        # Проверка, что второй пользователь получает ошибку доступа
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Проверка, что название цели не изменилось
        goal.refresh_from_db()
        assert goal.title != new_title

    def test_update_goal_editor_success(self, auth_client):
        """
        Юзер с ролью "редактор" может редактировать категорию
        """
        # Создание пользователей, доски, категории и цели
        user_1 = UserFactory()
        board, category = create_board_and_category(auth_client, user_1)
        goal = GoalFactory(category=category, user=user_1)

        # Создание второго пользователя
        user_2 = UserFactory()

        # Добавление второго пользователя в доску с ролью "редактор" (2)
        add_participant_to_board(board, user_2, 2)

        # Подготовка данных для обновления цели
        url = reverse('goals:goal_view', args=[goal.id])
        new_title = "Updated Goal"
        payload = {
            "title": new_title,
        }

        # Аутентификация второго пользователя
        auth_client.force_authenticate(user=user_2)

        # Отправка запроса на обновление цели
        response = auth_client.patch(url, data=payload)

        # Проверка, что второй пользователь может успешно обновить цель
        assert response.status_code == status.HTTP_200_OK

        # Проверка, что название цели изменилось
        goal.refresh_from_db()
        assert goal.title == new_title
