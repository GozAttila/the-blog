from blog.report.models import Report
from blog.blogs.models import Blog
from blog.comment.models import Comment
from .serializers import ReportSerializer

from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class ReportCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, content_type, object_id):
        user = request.user
        content_type = ContentType.objects.get(model=content_type)

        if Report.objects.filter(reported_by=user, content_type=content_type, object_id=object_id).exists():
            return Response(
                {'message': 'You have already reported this content.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        report = Report.objects.create(
            reported_by=user,
            content_type=content_type,
            object_id=object_id,
            reason=request.data.get('reason', ''),
            report_type=request.data.get('report_type', '')
        )
        return Response({'message': 'Report submitted successfully.'}, status=status.HTTP_201_CREATED)

class ReportListView(generics.ListAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to view reports.")
        return Report.objects.all()

class ReportActionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, report_id):
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to take action on reports.")

        report = get_object_or_404(Report, id=report_id)
        action = request.data.get('action')

        content_object = report.content_object
        if not hasattr(content_object, 'is_blocked'):
            return Response({'error': 'Invalid content type.'}, status=status.HTTP_400_BAD_REQUEST)

        if action == 'block':
            if content_object.is_blocked:
                return Response({'message': 'Content is already blocked and cannot be blocked again.'}, status=status.HTTP_403_FORBIDDEN)
            content_object.is_blocked = True
            content_object.blocked_by = request.user
            content_object.save()
            return Response({'message': 'Content has been blocked.'}, status=status.HTTP_200_OK)

        elif action == 'unblock':
            if not content_object.is_blocked:
                return Response({'message': 'Content is not blocked.'}, status=status.HTTP_400_BAD_REQUEST)
            content_object.is_blocked = False
            content_object.blocked_by = request.user
            content_object.save()
            return Response({'message': 'Content has been unblocked.'}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)
