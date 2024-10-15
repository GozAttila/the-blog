from .views import ManagementAddToBlacklistView, ManagementRemoveFromBlacklistView, ManagementAddToWhitelistView, ManagementRemoveFromWhitelistView

from django.urls import path

urlpatterns = [
    path('blacklist/add/', ManagementAddToBlacklistView.as_view(), name='management-add-to-blacklist'),
    path('blacklist/remove/', ManagementRemoveFromBlacklistView.as_view(), name='management-remove-from-blacklist'),
    path('whitelist/add/', ManagementAddToWhitelistView.as_view(), name='management-add-to-whitelist'),
    path('whitelist/remove/', ManagementRemoveFromWhitelistView.as_view(), name='management-remove-from-whitelist'),
]
