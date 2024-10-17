from blog.management.models import ChangeRequest
from blog.management.views import (
    ManagementAddToBlacklistView,
    ManagementRemoveFromBlacklistView,
    ManagementAddToWhitelistView,
    ManagementRemoveFromWhitelistView,
    ChangeRequestListView,
    ChangeRequestDetailView,
    ChangeRequestActionView,
    ChangeRequestCreateView
)
from blog.utils.blacklist import remove_from_file

from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class ViewsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', email='test@example.com')        
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', email='admin@example.com', is_staff=True)

        self.user_client = self.client_class()
        self.admin_client = self.client_class()

        self.user_client.force_authenticate(user=self.user)
        self.admin_client.force_authenticate(user=self.admin_user)

    def tearDown(self):
        remove_from_file('blacklist', 'newblackword')
        remove_from_file('whitelist', 'newwhiteword')

    def test_add_to_blacklist_view(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('management-add-to-blacklist')
        data = {'word': 'newblackword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with open('blog/utils/blacklists/blacklist.txt', 'r') as file:
            blacklist = file.read()
        self.assertIn('newblackword', blacklist)

    def test_remove_from_blacklist_view(self):
        self.client.force_authenticate(user=self.admin_user)
        url_add = reverse('management-add-to-blacklist')
        data_add = {'word': 'removeword'}
        self.client.post(url_add, data_add)

        url_remove = reverse('management-remove-from-blacklist')
        data_remove = {'word': 'removeword'}
        response = self.client.post(url_remove, data_remove)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with open('blog/utils/blacklists/blacklist.txt', 'r') as file:
            blacklist = file.read()
        self.assertNotIn('removeword', blacklist)

    def test_add_to_whitelist_view(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('management-add-to-whitelist')
        data = {'word': 'newwhiteword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with open('blog/utils/blacklists/whitelist.txt', 'r') as file:
            whitelist = file.read()
        self.assertIn('newwhiteword', whitelist)

    def test_remove_from_whitelist_view(self):
        self.client.force_authenticate(user=self.admin_user)
        url_add = reverse('management-add-to-whitelist')
        data_add = {'word': 'removewhiteword'}
        self.client.post(url_add, data_add)

        url_remove = reverse('management-remove-from-whitelist')
        data_remove = {'word': 'removewhiteword'}
        response = self.client.post(url_remove, data_remove)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with open('blog/utils/blacklists/whitelist.txt', 'r') as file:
            whitelist = file.read()
        self.assertNotIn('removewhiteword', whitelist)


    def test_change_request_create_view(self):
        url = reverse('change-request-create')
        data = {
            'request_type': 'email_change',
            'requested_email': 'newemail@example.com',
            'reason': 'I want to change my email.'
        }
        response = self.user_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ChangeRequest.objects.filter(user=self.user, requested_email='newemail@example.com').exists())

    def test_change_request_action_view_approve(self):
        change_request = ChangeRequest.objects.create(
            user=self.user,
            request_type='name_change',
            requested_name='New Name',
            reason='Requesting a name change'
        )
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('change-request-action', args=[change_request.id])
        response = self.client.patch(url, {'action': 'approve'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        change_request.refresh_from_db()
        self.assertTrue(change_request.is_approved)

    def test_change_request_action_view_deny(self):
        change_request = ChangeRequest.objects.create(
            user=self.user,
            request_type='email_change',
            requested_email='newemail@example.com',
            reason='Requesting an email change'
        )
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('change-request-action', args=[change_request.id])
        response = self.client.patch(url, {'action': 'deny'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        change_request.refresh_from_db()
        self.assertFalse(change_request.is_approved)

    def test_change_request_action_view_reopen(self):
        change_request = ChangeRequest.objects.create(
            user=self.user,
            request_type='name_change',
            requested_name='Old Name',
            reason='Requesting a name change',
            is_approved=False
        )
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('change-request-action', args=[change_request.id])
        response = self.client.patch(url, {'action': 'reopen'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        change_request.refresh_from_db()
        self.assertFalse(change_request.is_approved)

class URLsTests(APITestCase):
    def test_blacklist_add_url(self):
        url = reverse('management-add-to-blacklist')
        self.assertEqual(resolve(url).func.view_class, ManagementAddToBlacklistView)

    def test_blacklist_remove_url(self):
        url = reverse('management-remove-from-blacklist')
        self.assertEqual(resolve(url).func.view_class, ManagementRemoveFromBlacklistView)

    def test_whitelist_add_url(self):
        url = reverse('management-add-to-whitelist')
        self.assertEqual(resolve(url).func.view_class, ManagementAddToWhitelistView)

    def test_whitelist_remove_url(self):
        url = reverse('management-remove-from-whitelist')
        self.assertEqual(resolve(url).func.view_class, ManagementRemoveFromWhitelistView)

    def test_change_request_list_url(self):
        url = reverse('change-request-list')
        self.assertEqual(resolve(url).func.view_class, ChangeRequestListView)

    def test_change_request_detail_url(self):
        url = reverse('change-request-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, ChangeRequestDetailView)

    def test_change_request_action_url(self):
        url = reverse('change-request-action', args=[1])
        self.assertEqual(resolve(url).func.view_class, ChangeRequestActionView)

    def test_change_request_create_url(self):
        url = reverse('change-request-create')
        self.assertEqual(resolve(url).func.view_class, ChangeRequestCreateView)
