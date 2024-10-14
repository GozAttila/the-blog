from .models import Report

from rest_framework import serializers

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'reported_by', 'content_type', 'object_id', 'reason', 'created_at']
        read_only_fields = ['id', 'reported_by', 'created_at']
