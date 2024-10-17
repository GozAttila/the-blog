from .views import (
    ManagementAddToBlacklistView,
    ManagementRemoveFromBlacklistView,
    ManagementAddToWhitelistView,
    ManagementRemoveFromWhitelistView,
    ChangeRequestListView,
    ChangeRequestDetailView,
    ChangeRequestActionView,
    ChangeRequestCreateView,
)

from django.urls import path

urlpatterns = [
    path('blacklist/add/', ManagementAddToBlacklistView.as_view(), name='management-add-to-blacklist'),
    path('blacklist/remove/', ManagementRemoveFromBlacklistView.as_view(), name='management-remove-from-blacklist'),
    path('whitelist/add/', ManagementAddToWhitelistView.as_view(), name='management-add-to-whitelist'),
    path('whitelist/remove/', ManagementRemoveFromWhitelistView.as_view(), name='management-remove-from-whitelist'),
    path('requests/create/', ChangeRequestCreateView.as_view(), name='change-request-create'),
    path('requests/', ChangeRequestListView.as_view(), name='change-request-list'),
    path('requests/<int:pk>/', ChangeRequestDetailView.as_view(), name='change-request-detail'),
    path('requests/<int:pk>/action/', ChangeRequestActionView.as_view(), name='change-request-action'),
]
