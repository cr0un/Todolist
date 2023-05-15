from typing import Callable
import pytest
from django.urls import reverse
from rest_framework import status
from goals.models import BoardParticipant


@pytest.fixture
def board_create_data(faker) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {'title': faker.sentence(2)}
        data |= kwargs
        return data
    return _wrapper


@pytest.mark.django_db
class TestBoardCreateView:
    url = reverse('goals:create_board')

    def test_auth_required(self, client, board_create_data):
        """
        Неавторизованный пользователь при создании доски получит ошибку авторизации
        """
        response = client.post(self.url, data=board_create_data())
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_create_deleted_board(self, auth_client, board_create_data):
        """
        Нельзя создать удаленную доску
        """
        data = board_create_data(is_deleted=True)
        response = auth_client.post(self.url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()['is_deleted'] == ['Некорректное значение is_deleted']

    def test_request_user_is_owner(self, auth_client, board_create_data, user):
        """
        Пользователь создал доску и стал ее владельцем
        """
        response = auth_client.post(self.url, data=board_create_data())
        assert response.status_code == status.HTTP_201_CREATED
        board_participant = BoardParticipant.objects.get(user_id=user.id)
        assert board_participant.board_id == response.data['id']
        assert board_participant.role == BoardParticipant.Role.owner




