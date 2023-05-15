from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework import permissions

from django.db import transaction
from rest_framework.permissions import IsAuthenticated

from goals.models import Board, Goal, BoardParticipant
from goals.permissions import BoardPermissions
from goals.serializers import BoardSerializer, BoardCreateSerializer, BoardListSerializer


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance


class BoardCreateView(CreateAPIView):
    serializer_class = BoardCreateSerializer
    permission_classes = [IsAuthenticated, ]


class BoardListView(ListAPIView):
    model = Board
    serializer_class = BoardListSerializer
    permission_classes = [BoardPermissions, ]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.prefetch_related('participants').filter(
            participants__user_id=self.request.user.id,
            is_deleted=False
        )


def check_goal_permission(user, goal_category):
    return BoardParticipant.objects.filter(
        user=user,
        board=goal_category.board,
        role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
    ).exists()
