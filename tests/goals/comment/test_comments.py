import pytest
from rest_framework import status
from goals.models import GoalComment
from tests.goals.test_utils import create_board_category_goal, create_board_category_goal_comment
from django.urls import reverse


@pytest.mark.django_db
class TestCommentsView:
    def test_create_goal_comment_success(self, auth_client, user):
        """
        Проверка добавление комментария
        """
        # Создание доски, категории и цели
        board, category, goal = create_board_category_goal(auth_client, user)

        # Подготовка данных для создания комментария
        goal_id = goal.id
        comment_text = "Test Comment"
        payload = {
            "goal": goal_id,
            "text": comment_text,
        }

        # Отправка запроса на создание комментария
        url = reverse("goals:goal_comment_create")
        response = auth_client.post(url, data=payload)

        # Проверка статуса ответа и наличия созданного комментария в базе данных
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data

        # Проверка, что комментарий был успешно создан с правильными значениями полей
        comment_id = response.data["id"]
        comment = GoalComment.objects.get(id=comment_id)
        assert comment.goal_id == goal_id
        assert comment.text == comment_text

    def test_update_goal_comment_edit_success(self, auth_client, user):
        """
        Проверка редактирования комментария
        """
        # Создание доски, категории, цели и комментария
        board, category, goal, comment = create_board_category_goal_comment(auth_client, user)

        # Подготовка данных для обновления комментария
        comment_id = comment.id
        new_text = "Updated Comment"
        payload = {
            "text": new_text,
        }

        # Отправка запроса на обновление комментария
        url = reverse("goals:goal_comment_view", args=[comment_id])
        response = auth_client.patch(url, data=payload)

        # Проверка статуса ответа и обновления комментария в базе данных
        assert response.status_code == status.HTTP_200_OK
        assert response.data["text"] == new_text
        assert GoalComment.objects.get(id=comment_id).text == new_text

    def test_delete_goal_comment_success(self, auth_client, user):
        """
        Проверка удаления комментария
        """
        # Создание доски, категории, цели и комментария
        board, category, goal = create_board_category_goal(auth_client, user)
        comment_text = "Test Comment"
        comment = GoalComment.objects.create(goal=goal, text=comment_text, user=user)

        # Подготовка данных для удаления комментария
        url = reverse("goals:goal_comment_view", args=[comment.id])

        # Отправка запроса на удаление комментария
        response = auth_client.delete(url)

        # Проверка статуса ответа и проверка, что комментарий был удален
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not GoalComment.objects.filter(id=comment.id).exists()
