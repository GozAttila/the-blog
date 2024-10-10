from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from blog.like.models import Like
from django.contrib.contenttypes.models import ContentType

class LikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, content_type, object_id):
        user = request.user
        content_type = ContentType.objects.get(model=content_type)
        
        like, created = Like.objects.get_or_create(
            user=user, 
            content_type=content_type, 
            object_id=object_id
        )

        if not created:
            # Like already exists, so we toggle it
            like.delete()
            return Response({'message': 'Like removed.'}, status=status.HTTP_200_OK)
        
        like.is_like = request.data.get('is_like', True)
        like.save()
        return Response({'message': 'Like added.'}, status=status.HTTP_201_CREATED)
