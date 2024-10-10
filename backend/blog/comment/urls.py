from django.urls import path
from .views import CommentCreateView

urlpatterns = [
    path('create/<int:blog_id>/', CommentCreateView.as_view(), name='api-comment-create'),
]
