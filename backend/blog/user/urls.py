from .views import register_user, CustomAuthToken, validate_username

from django.urls import path

urlpatterns = [
    path('register/', register_user, name='api-register'),
    path('login/', CustomAuthToken.as_view(), name='api-login'),
    path('validate-username/', validate_username, name='api-validate-username'),
]
