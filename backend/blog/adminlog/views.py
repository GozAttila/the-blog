from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import AdminMessage
from .serializers import AdminMessageSerializer

class AdminMessageCreateView(generics.CreateAPIView):
    serializer_class = AdminMessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        reply_to = serializer.validated_data.get('reply_to')
        if reply_to:
            # Csak a címzett válaszolhat az eredeti üzenetre
            if reply_to.recipient != self.request.user:
                raise PermissionDenied("You are not allowed to reply to this message.")
            serializer.save(sender=self.request.user, recipient=reply_to.sender)
        else:
            # Csak admin küldhet új üzenetet
            if not self.request.user.is_staff:
                raise PermissionDenied("Only admins can send new messages.")
            serializer.save(sender=self.request.user)

class AdminMessageListView(generics.ListAPIView):
    serializer_class = AdminMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AdminMessage.objects.filter(recipient=self.request.user)
