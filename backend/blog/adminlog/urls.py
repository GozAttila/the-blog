from django.urls import path
from .views import AdminMessageCreateView, AdminMessageListView

urlpatterns = [
    path('messages/send/', AdminMessageCreateView.as_view(), name='admin-message-send'),
    path('messages/', AdminMessageListView.as_view(), name='admin-message-list'),
]
