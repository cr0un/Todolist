from django.urls import path
from goals import views
from goals.views import GoalCommentCreateView, GoalCommentListView, GoalCommentView

urlpatterns = [
    path("goal_category/create", views.GoalCategoryCreateView.as_view()),
    path("goal_category/list", views.GoalCategoryListView.as_view()),
    path("goal_category/<pk>", views.GoalCategoryView.as_view()),

    path("goal/create", views.GoalCreateView.as_view()),
    path("goal/list", views.GoalListView.as_view()),
    path("goal/<pk>", views.GoalView.as_view()),

    path("goals/goal_comment/create", GoalCommentCreateView.as_view(), name="goal_comment_create"),
    path("goals/goal_comment/list", GoalCommentListView.as_view(), name="goal_comment_list"),
    path("goals/goal_comment/<int:pk>", GoalCommentView.as_view(), name="goal_comment_view"),
]