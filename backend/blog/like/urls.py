from django.urls import path
from .views import LikeToggleView

urlpatterns = [
    path('toggle/<str:content_type>/<int:object_id>/', LikeToggleView.as_view(), name='api-like-toggle'),
]
