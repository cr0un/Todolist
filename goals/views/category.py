from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from goals.models import GoalCategory, BoardParticipant, Board

from django_filters.rest_framework import DjangoFilterBackend

from goals.permissions import IsBoardOwnerOrEditor
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsBoardOwnerOrEditor]

    def perform_create(self, serializer):
        board = serializer.validated_data["board"]
        if not board.participants.filter(user=self.request.user).exclude(
                role=BoardParticipant.Role.reader
        ).exists():
            raise PermissionDenied("Вы должны быть владельцем или редактором")
        serializer.save()


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_boards = Board.objects.filter(participants__user=self.request.user)
        return GoalCategory.objects.filter(board__in=user_boards, is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["board"]


    def get_queryset(self):
        user_boards = Board.objects.filter(participants__user=self.request.user)
        return GoalCategory.objects.filter(board__in=user_boards, is_deleted=False)


    def perform_destroy(self, instance):
        board = instance.board
        if not board.participants.filter(user=self.request.user).exclude(
                role=BoardParticipant.Role.reader
        ).exists():
            raise PermissionDenied("Вы должны быть владельцем или редактором")

    def perform_update(self, serializer):
        board = self.get_object().board
        if not board.participants.filter(user=self.request.user).exclude(
                role=BoardParticipant.Role.reader
        ).exists():
            raise PermissionDenied("Вы должны быть владельцем или редактором")
        serializer.save()