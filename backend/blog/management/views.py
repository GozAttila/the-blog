from blog.utils.blacklist import add_to_file, remove_from_file

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

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
