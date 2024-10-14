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

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        reply_to = data.get('reply_to')
        user = self.context['request'].user
        if reply_to and reply_to.recipient != user:
            raise serializers.ValidationError("You cannot reply to a message that is not addressed to you.")

        if not reply_to and not user.is_staff:
            raise serializers.ValidationError("Only admins can send new messages.")

        return data
