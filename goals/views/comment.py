from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from goals.models import GoalComment, Goal, BoardParticipant
from goals.serializers import GoalCommentCreateSerializer, GoalCommentSerializer


class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    serializer_class = GoalCommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        goal_id = self.request.data.get("goal")
        goal = Goal.objects.get(id=goal_id)
        user_boards = BoardParticipant.objects.filter(
            user=self.request.user
        ).exclude(role=BoardParticipant.Role.reader).values_list('board_id', flat=True)

        if goal.category.board.id in user_boards:
            serializer.save()
        else:
            raise PermissionDenied("У вас нет прав для создания комментария к этой цели")


class GoalCommentListView(ListAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["created"]
    filterset_fields = ["goal"]

    def get_queryset(self):
        user_boards = BoardParticipant.objects.filter(user=self.request.user).values_list('board_id', flat=True)
        return GoalComment.objects.filter(goal__category__board__id__in=user_boards)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        user = self.request.user
        user_boards = BoardParticipant.objects.filter(
            user=user
        ).exclude(role=BoardParticipant.Role.reader).values_list('board_id', flat=True)
        goals = Goal.objects.filter(category__board_id__in=user_boards)
        return GoalComment.objects.filter(goal__in=goals)