from .views import LikeToggleView

from django.urls import path

urlpatterns = [
    path('toggle/<str:content_type>/<int:object_id>/', LikeToggleView.as_view(), name='api-like-toggle'),
]
