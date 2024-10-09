from .models import Invitation
from .models import Blog

from rest_framework import serializers

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'author', 'title', 'content', 'is_private', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']

class InvitationAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['is_accepted']
