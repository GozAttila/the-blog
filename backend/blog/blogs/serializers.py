from .models import Blog, BlogTranslation, Invitation

from rest_framework import serializers

class BlogSerializer(serializers.ModelSerializer):
    blocked_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'author', 'title', 'content', 'is_private', 'is_blocked', 'blocked_by', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at', 'blocked_by']

class InvitationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['blog', 'invited_user', 'invited_by']
        read_only_fields = ['invited_by']

class InvitationAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['is_accepted']

class BlogTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTranslation
        fields = ['id', 'language', 'translated_title', 'translated_content']
