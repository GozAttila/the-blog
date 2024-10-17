from .models import ChangeRequest

from rest_framework import serializers

class ChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeRequest
        fields = [
            'id', 'user', 'request_type', 'requested_name', 
            'requested_email', 'reason', 'is_approved', 'is_archived', 
            'changelog', 'created_at', 'updated_at', 'handled_by', 'handled_at'
        ]
        read_only_fields = ['id', 'is_approved', 'is_archived', 'changelog', 'created_at', 'updated_at', 'handled_by', 'handled_at', 'user']

class ChangeRequestActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'deny', 'reopen'])
