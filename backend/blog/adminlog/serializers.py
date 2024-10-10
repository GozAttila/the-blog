from .models import AdminMessage

from rest_framework import serializers

class AdminMessageSerializer(serializers.ModelSerializer):
    reply_to = serializers.PrimaryKeyRelatedField(
        queryset=AdminMessage.objects.all(), 
        required=False, 
        allow_null=True
    )

    class Meta:
        model = AdminMessage
        fields = ['id', 'sender', 'recipient', 'subject', 'body', 'is_read', 'created_at', 'reply_to']
        read_only_fields = ['sender', 'created_at']
