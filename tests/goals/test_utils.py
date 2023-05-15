from django.urls import reverse
from goals.models import Board, GoalCategory, BoardParticipant, Goal, GoalComment
from tests.factories import BoardFactory


def create_board_and_category(client, user):
    """
    Создание доски
    """
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


def create_board_category_goal(client, user):
    """
    Создание доски, категории и цели
    """
    board = BoardFactory()
    payload_board = {
        "title": "Test Board",
        "board": board.id,
    }
    url_create_board = reverse("goals:create_board")
    client.force_authenticate(user=user)
    response = client.post(url_create_board, data=payload_board)
    created_board_id = response.json()["id"]
    board = Board.objects.get(id=created_board_id)

    # Создание категории в доске
    payload_category = {
        "title": "Test Category",
        "board": board.id,
    }
    url_create_goal_category = reverse("goals:create_goal_category")
    response = client.post(url_create_goal_category, data=payload_category)
    created_category_id = response.json()["id"]
    category = GoalCategory.objects.get(id=created_category_id)

    # Создание цели в категории
    payload_goal = {
        "title": "Test Goal",
        "description": "Test Description",
        "category": category.id,
    }
    url_create_goal = reverse("goals:goal_create")
    response = client.post(url_create_goal, data=payload_goal)
    created_goal_id = response.json()["id"]
    goal = Goal.objects.get(id=created_goal_id)

    return board, category, goal


def create_board_category_goal_comment(client, user):
    """
    Создание доски, категории, цели и комментария
    """
    board, category, goal = create_board_category_goal(client, user)

    # Создание комментария к цели
    payload_comment = {
        "text": "Test Comment",
        "goal": goal.id,
    }
    url_create_comment = reverse("goals:goal_comment_create")
    response = client.post(url_create_comment, data=payload_comment)
    created_comment_id = response.json()["id"]
    comment = GoalComment.objects.get(id=created_comment_id)
    return board, category, goal, comment


def add_participant_to_board(board, user, role):
    """
    Функция добавления участника к доске с указанием роли.
    Роль пользователя на доске (1 - админ, 2 - редактор, 3 - читатель)
    """
    BoardParticipant.objects.create(
        board=board,
        user=user,
        role=role,
    )
