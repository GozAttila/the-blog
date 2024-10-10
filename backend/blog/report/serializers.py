from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'reported_by', 'content_type', 'object_id', 'reason', 'created_at']
