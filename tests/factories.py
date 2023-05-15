import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from factory import Faker
from core.models import User
from pytest_factoryboy import register
from goals.models import Board, GoalCategory, Goal


@register
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('user_name')
    password = Faker('password')

    # email = ''

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # return cls._get_manager(model_class).create_user(*args, **kwargs)
        return User.objects.create_user(*args, **kwargs)


class DatesFactoryMixin(DjangoModelFactory):
    class Meta:
        abstract = True

    created = factory.LazyFunction(timezone.now)
    updated = factory.LazyFunction(timezone.now)


@register
class BoardFactory(DatesFactoryMixin):
    title = factory.Faker('sentence')

    class Meta:
        model = Board


@register
class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = factory.Faker("sentence")
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)


@register
class GoalFactory(DatesFactoryMixin):
    title = factory.Faker('sentence')
    description = factory.Faker('text')
    category = factory.SubFactory(GoalCategoryFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Goal

