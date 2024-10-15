from blog.comment.models import Comment

from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    blocked_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'blog', 'content', 'is_blocked', 'blocked_by', 'created_at']
        read_only_fields = ['author', 'blog', 'created_at', 'blocked_by']
