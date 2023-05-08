from rest_framework import permissions
from goals.models import BoardParticipant, Board, GoalCategory, Goal


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class IsBoardOwnerOrEditor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        board_id = request.data.get("board", None)
        if not board_id:
            return False

        try:
            board = Board.objects.get(pk=board_id)
        except Board.DoesNotExist:
            return False

        return board.participants.filter(
            user=request.user
        ).exclude(role=BoardParticipant.Role.reader).exists()

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not isinstance(obj, GoalCategory):
            return False

        return obj.board.participants.filter(
            user=request.user
        ).exclude(role=BoardParticipant.Role.reader).exists()


class IsGoalOwnerOrEditor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not isinstance(obj, Goal):
            return False

        return obj.category.board.participants.filter(
            user=request.user
        ).exclude(role=BoardParticipant.Role.reader).exists()
