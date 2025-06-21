from rest_framework.urls import path

from task.views import PostRetrieveUpdateDestroyView, PostListCreateView, CommentListCreateView, CommentDeleteView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comment/', CommentListCreateView.as_view(), name='comment_get_post'),
    path('comments/<int:id>/', CommentDeleteView.as_view(), name='comment_delete'),

]