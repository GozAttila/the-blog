from .models import Blog, Invitation, User
from .serializers import BlogSerializer, InvitationAcceptSerializer, UserRegistrationSerializer

from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        return Response({'token': token.key, 'user_id': user.id, 'username': user.username})

class BlogListCreateView(generics.ListCreateAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = Blog.objects.filter(is_private=False)

        if user.is_authenticated:
            invited_blogs = Blog.objects.filter(
                invitation__invited_user=user,
                invitation__is_accepted=True
            )
            queryset = queryset | Blog.objects.filter(author=user) | invited_blogs

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Blog.objects.filter(is_private=False)

        if user.is_authenticated:
            invited_blogs = Blog.objects.filter(
                invitation__invited_user=user,
                invitation__is_accepted=True
            )
            queryset = queryset | Blog.objects.filter(author=user) | invited_blogs

        return queryset
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])

        # További jogosultságok ellenőrzése a privát blogok esetében.
        if obj.is_private:
            if obj.author != self.request.user:
                raise PermissionDenied("You do not have permission to view this private blog.")
        return obj

class InvitationAcceptView(APIView):
    def post(self, request, pk):
        try:
            invitation = Invitation.objects.get(pk=pk, invited_user=request.user)
            serializer = InvitationAcceptSerializer(invitation, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Invitation status updated successfully.'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Invitation.DoesNotExist:
            return Response({'error': 'Invitation not found or you do not have permission to update this invitation.'},
                            status=status.HTTP_404_NOT_FOUND)
