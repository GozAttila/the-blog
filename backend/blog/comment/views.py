from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from blog.comment.models import Comment
from blog.comment.serializers import CommentSerializer
from blog.blogs.models import Blog

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        blog = Blog.objects.get(pk=self.kwargs['blog_id'])
        user = self.request.user

        # Ellenőrzés: felhasználó a blog szerzője vagy elfogadott meghívott?
        if blog.is_private and not (
            blog.author == user or
            blog.invitation_set.filter(invited_user=user, is_accepted=True).exists()
        ):
            return Response(
                {'detail': 'You do not have permission to comment on this blog.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save(author=user, blog=blog)
