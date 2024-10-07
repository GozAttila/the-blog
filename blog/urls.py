from django.urls import path
from .views import register_user, CustomAuthToken

urlpatterns = [
    path('api/register/', register_user, name='api-register'),
    path('api/login/', CustomAuthToken.as_view(), name='api-login'),
]
