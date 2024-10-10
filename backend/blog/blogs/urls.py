from .views import BlogDetailView, BlogListCreateView, InvitationAcceptView, InvitationCreateView, BlogTranslationView

from django.urls import path

urlpatterns = [
    path('', BlogListCreateView.as_view(), name='api-blog-list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='api-blog-detail'),
    path('invite/<int:blog_id>/', InvitationCreateView.as_view(), name='api-invitation-create'),
    path('invitations/<int:pk>/accept/', InvitationAcceptView.as_view(), name='api-invitation-accept'),
    path('translation/<int:pk>/', BlogTranslationView.as_view(), name='api-blog-translation'),
]
