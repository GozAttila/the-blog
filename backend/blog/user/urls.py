from .views import register_user, CustomAuthToken

from django.urls import path

urlpatterns = [
    path('register/', register_user, name='api-register'),
    path('login/', CustomAuthToken.as_view(), name='api-login'),
]
