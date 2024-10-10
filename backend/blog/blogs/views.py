from .models import Blog, BlogTranslation, Invitation
from .serializers import BlogSerializer, InvitationAcceptSerializer

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

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

    def get_object(self):
        obj = get_object_or_404(Blog, pk=self.kwargs['pk'])

        if obj.is_private and obj.author != self.request.user and not obj.invitation_set.filter(
                invited_user=self.request.user, is_accepted=True).exists():
            raise PermissionDenied("You do not have permission to view this private blog.")

        if obj.is_blocked and obj.author != self.request.user:
            raise PermissionDenied("You do not have permission to view this blocked blog.")

        return obj

class InvitationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, blog_id):
        blog = get_object_or_404(Blog, id=blog_id)

        if blog.author != request.user:
            raise PermissionDenied("You do not have permission to send invitations for this blog.")

        invited_user_id = request.data.get('invited_user_id')
        invited_user = get_object_or_404(settings.AUTH_USER_MODEL, id=invited_user_id)

        if Invitation.objects.filter(blog=blog, invited_user=invited_user).exists():
            raise ValidationError("This user is already invited to the blog.")

        invitation = Invitation.objects.create(
            blog=blog,
            invited_user=invited_user,
            invited_by=request.user,
        )
        return Response(
            {'message': 'Invitation sent successfully.', 'invitation_id': invitation.id},
            status=status.HTTP_201_CREATED
        )

class InvitationAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        invitation = get_object_or_404(Invitation, pk=pk, invited_user=request.user,)
        
        if invitation.is_accepted:
            return Response(
                {'message': 'Invitation has already been accepted.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = InvitationAcceptSerializer(invitation, data={'is_accepted': True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Invitation accepted successfully.'},
                status=status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )

class BlogTranslationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)

        if blog.author != request.user:
            raise PermissionDenied("You do not have permission to translate this blog.")

        translation = BlogTranslation.objects.create(
            blog=blog,
            language=request.data.get('language', ''),
            translated_title=request.data.get('translated_title', ''),
            translated_content=request.data.get('translated_content', '')
        )

        return Response(
            {'message': 'Translation created successfully.'},
            status=status.HTTP_201_CREATED
        )
