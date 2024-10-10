from blog.blogs.models import Blog
from blog.comment.models import Comment
from blog.comment.serializers import CommentSerializer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        blog = Blog.objects.get(pk=self.kwargs['blog_id'])
        user = self.request.user

        if blog.is_private and not (
            blog.author == user or
            blog.invitation_set.filter(invited_user=user, is_accepted=True).exists()
        ):
            raise PermissionDenied("You do not have permission to comment on this blog.")

        serializer.save(author=user, blog=blog)

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        blog_id = self.kwargs.get('blog_id')
        blog = Blog.objects.get(id=blog_id)

        if blog.is_private and not (
            blog.author == self.request.user or
            blog.invitation_set.filter(invited_user=self.request.user, is_accepted=True).exists()
        ):
            raise PermissionDenied("You do not have permission to view comments for this blog.")

        return Comment.objects.filter(blog=blog)
