from django.urls import path
from .views import CommentCreateView, CommentListView

urlpatterns = [
    path('create/<int:blog_id>/', CommentCreateView.as_view(), name='api-comment-create'),
    path('list/<int:blog_id>/', CommentListView.as_view(), name='api-comment-list'),
]
