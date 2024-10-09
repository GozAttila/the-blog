from .views import BlogDetailView, BlogListCreateView, InvitationAcceptView

from django.urls import path

urlpatterns = [
    path('', BlogListCreateView.as_view(), name='api-blog-list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='api-blog-detail'),
    path('invitations/<int:pk>/accept/', InvitationAcceptView.as_view(), name='api-invitation-accept'),    
]
