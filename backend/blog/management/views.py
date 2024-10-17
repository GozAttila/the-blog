from blog.management.models import ChangeRequest
from blog.management.serializers import ChangeRequestActionSerializer, ChangeRequestSerializer
from blog.utils.blacklist import add_to_file, remove_from_file

from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class ManagementAddToBlacklistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        word = request.data.get('word', '').strip().lower()
        if word:
            add_to_file('blacklist', word)
            return Response({'message': f'{word} added to blacklist.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No word provided.'}, status=status.HTTP_400_BAD_REQUEST)

class ManagementRemoveFromBlacklistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        word = request.data.get('word', '').strip().lower()
        if word:
            remove_from_file('blacklist', word)
            return Response({'message': f'{word} removed from blacklist.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No word provided.'}, status=status.HTTP_400_BAD_REQUEST)

class ManagementAddToWhitelistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        word = request.data.get('word', '').strip().lower()
        if word:
            add_to_file('whitelist', word)
            return Response({'message': f'{word} added to whitelist.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No word provided.'}, status=status.HTTP_400_BAD_REQUEST)

class ManagementRemoveFromWhitelistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        word = request.data.get('word', '').strip().lower()
        if word:
            remove_from_file('whitelist', word)
            return Response({'message': f'{word} removed from whitelist.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No word provided.'}, status=status.HTTP_400_BAD_REQUEST)

class ChangeRequestCreateView(generics.CreateAPIView):
    serializer_class = ChangeRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChangeRequestListView(generics.ListAPIView):
    queryset = ChangeRequest.objects.all()
    serializer_class = ChangeRequestSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        request_type = self.request.query_params.get('request_type')
        is_archived = self.request.query_params.get('is_archived')
        queryset = super().get_queryset()
        if request_type:
            queryset = queryset.filter(request_type=request_type)
        if is_archived is not None:
            queryset = queryset.filter(is_archived=is_archived.lower() == 'true')
        return queryset

class ChangeRequestDetailView(generics.RetrieveAPIView):
    queryset = ChangeRequest.objects.all()
    serializer_class = ChangeRequestSerializer
    permission_classes = [IsAdminUser]

class ChangeRequestActionView(generics.UpdateAPIView):
    serializer_class = ChangeRequestActionSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        change_request = get_object_or_404(ChangeRequest, pk=kwargs.get('pk'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = serializer.validated_data['action']
        if action == 'approve':
            change_request.approve(request.user)
        elif action == 'deny':
            change_request.deny(request.user)
        elif action == 'reopen':
            change_request.reopen(request.user)

        return Response({'status': 'success'}, status=status.HTTP_200_OK)
