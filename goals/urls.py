from django.urls import path
from goals.views import category, comment, goal, board

app_name = 'goals'

urlpatterns = [
    path('goal_category/create', category.GoalCategoryCreateView.as_view(), name='create_goal_category'),
    path('goal_category/list', category.GoalCategoryListView.as_view(), name='list_goal_category'),
    path('goal_category/<pk>', category.GoalCategoryView.as_view(), name='retrieve_update_destroy_goal_category'),

    path('goal/create', goal.GoalCreateView.as_view(), name='goal_create'),
    path('goal/list', goal.GoalListView.as_view(), name='goal_list'),
    path('goal/<pk>', goal.GoalView.as_view(), name='goal_view'),

    path('goal_comment/create', comment.GoalCommentCreateView.as_view(), name='goal_comment_create'),
    path('goal_comment/list', comment.GoalCommentListView.as_view(), name='goal_comment_list'),
    path('goal_comment/<int:pk>', comment.GoalCommentView.as_view(), name='goal_comment_view'),

    path('board/create', board.BoardCreateView.as_view(), name='create_board'),
    path('board/list', board.BoardListView.as_view(), name='board_list'),
    path('board/<int:pk>', board.BoardView.as_view(), name='board_view'),
]