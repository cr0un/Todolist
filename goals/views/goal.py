from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import Goal
from goals.permissions import IsGoalOwnerOrEditor
from goals.serializers import GoalCreateSerializer, GoalSerializer
from goals.views.board import check_goal_permission


class GoalCreateView(CreateAPIView):
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        goal_category = serializer.validated_data["category"]
        if check_goal_permission(self.request.user, goal_category):
            serializer.save(user=self.request.user)
        else:
            raise PermissionDenied("Недостаточно прав для создания цели в данной категории")


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated, IsGoalOwnerOrEditor]
    lookup_field = "pk"

    def get_queryset(self):
        return Goal.objects.filter(
            is_deleted=False,
            category__is_deleted=False,
            category__board__participants__user=self.request.user
        )

    def perform_update(self, serializer):
        goal = self.get_object()
        if check_goal_permission(self.request.user, goal.category):
            serializer.save()
        else:
            raise PermissionDenied("Недостаточно прав для редактирования этой цели")

    def perform_destroy(self, instance):
        if check_goal_permission(self.request.user, instance.category):
            instance.is_deleted = True
            instance.save()
        else:
            raise PermissionDenied("Недостаточно прав для удаления этой цели")
        return instance


class GoalListView(ListAPIView):
    model = Goal
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = GoalDateFilter
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created"]

    # filterset_fields = {"category": ["exact", "in"]}
    filterset_fields = {"category": ["exact", "in"]}

    def get_queryset(self):
        return Goal.objects.filter(
            is_deleted=False,
            category__is_deleted=False,
            category__board__participants__user=self.request.user
        )
