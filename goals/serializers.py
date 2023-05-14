from django.db import transaction
from rest_framework import serializers

from core.models import User
from core.serializers import UserSerializer
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_deleted = serializers.BooleanField(default=False)
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    board = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("Не доступно в удаленной категории")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("Вы не владелец категории")

        return value


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_deleted = serializers.BooleanField(default=False)

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("Не доступно в удаленной категории")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("Вы не владелец категории")

        return value


class GoalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = GoalCategorySerializer(read_only=True)
    status = serializers.ChoiceField(choices=Goal.Status.choices)
    priority = serializers.ChoiceField(choices=Goal.Priority.choices)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    # class Meta:
    #     model = Board
    #     read_only_fields = ("id", "created", "updated")
    #     exclude = ("is_deleted",)
    #     extra_kwargs = {
    #         "is_deleted": {"default": serializers.CreateOnlyDefault(False)}
    #     }

    def validate_is_deleted(self, value):
        if value:
            raise serializers.ValidationError("Некорректное значение is_deleted")
        return value

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.Role.choices[1:]
    )

    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance, validated_data):
        owner: User = validated_data.pop('user')
        new_participants = validated_data.pop('participants')
        old_participants = instance.participants.exclude(user=owner)
        new_by_id = {part['user'].id: part for part in new_participants}
        with transaction.atomic():
            # определить и выкинуть тех, кого не будет в новом списке участников
            for old_part in old_participants:
                if old_part.user_id not in new_by_id.keys():
                    old_part.delete()
                # для всех, кто остался
                else:
                    # проверяем, изменилась ли роль -> изменяем
                    if old_part.role != new_by_id[old_part.user_id]['role']:
                        old_part.role = new_by_id[old_part.user_id]['role']
                        old_part.save()
                    # получаем обработанного старого участника и удаляем из словаря новых
                    new_by_id.pop(old_part.user_id)
            # для всех, кто остался в новых
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    user=new_part['user'],
                    board=instance,
                    role=new_part['role']
                )

                if title := validated_data.get('title'):
                    instance.title = title
                    instance.save()

        return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'
