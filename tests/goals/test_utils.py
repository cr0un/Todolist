from django.urls import reverse
from goals.models import Board, GoalCategory, BoardParticipant
from tests.factories import BoardFactory


def create_board_and_category(client, user):
    # Создание доски
    board = BoardFactory()
    payload_board = {
        "title": "Test Board",
        "board": board.id,
    }
    url_create_board = reverse("goals:create_board")
    client.force_authenticate(user=user)
    response = client.post(url_create_board, data=payload_board)
    created_board_id = response.json()["id"]  # Получаем ID созданной доски
    board = Board.objects.get(id=created_board_id)  # Обновляем переменную board

    # Создание категории в доске
    payload_category = {
        "title": "Test Category",
        "board": board.id,
    }
    url_create_goal_category = reverse("goals:create_goal_category")
    response = client.post(url_create_goal_category, data=payload_category)
    created_category_id = response.json()["id"]  # Получаем ID созданной категории
    category = GoalCategory.objects.get(id=created_category_id)  # Обновляем переменную category

    return board, category

def add_participant_to_board(board, user, role):
    """
    Функция добавления участника к доске с указанием роли.
    :param board: доска, к которой добавляется участник
    :param user: пользователь, которого нужно добавить к доске
    :param role: роль пользователя на доске (1 - админ, 2 - редактор, 3 - читатель)
    :return: None
    """
    BoardParticipant.objects.create(
        board=board,
        user=user,
        role=role,
    )