from blog.like.models import Like
from blog.like.serializers import LikeToggleSerializer

from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class LikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, content_type, object_id):
        serializer = LikeToggleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        content_type = ContentType.objects.get(model=content_type)
        is_like = serializer.validated_data['is_like']

        existing_like = Like.objects.filter(
            user=user,
            content_type=content_type,
            object_id=object_id
        ).first()

        if existing_like:
            if existing_like.is_like == is_like:
                existing_like.delete()
                return Response({'message': 'Reaction removed.'}, status=status.HTTP_200_OK)
            else:
                existing_like.is_like = is_like
                existing_like.save()
                return Response({'message': 'Reaction updated.'}, status=status.HTTP_200_OK)

        Like.objects.create(
            user=user,
            content_type=content_type,
            object_id=object_id,
            is_like=is_like
        )
        return Response({'message': 'Reaction added.'}, status=status.HTTP_201_CREATED)
