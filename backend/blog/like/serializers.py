from blog.like.models import Like

from rest_framework import serializers

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'content_type', 'object_id', 'is_like', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class LikeToggleSerializer(serializers.Serializer):
    is_like = serializers.BooleanField()
