from django.urls import path
from .views import BlogDetailView, BlogListCreateView, InvitationAcceptView, register_user, CustomAuthToken

urlpatterns = [
    path('api/register/', register_user, name='api-register'),
    path('api/login/', CustomAuthToken.as_view(), name='api-login'),
    path('api/blogs/', BlogListCreateView.as_view(), name='api-blog-list'),
    path('api/blogs/<int:pk>/', BlogDetailView.as_view(), name='api-blog-detail'),
    path('api/invitations/<int:pk>/accept/', InvitationAcceptView.as_view(), name='api-invitation-accept'),    
]
