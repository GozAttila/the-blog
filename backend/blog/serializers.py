from rest_framework import serializers
from .models import Invitation, User
from .models import Blog

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'author', 'title', 'content', 'is_private', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']

class InvitationAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['is_accepted']
