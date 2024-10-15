from blog.utils.blacklist import remove_from_file
from blog.management.views import ManagementAddToBlacklistView, ManagementAddToWhitelistView, ManagementRemoveFromBlacklistView, ManagementRemoveFromWhitelistView

from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class ViewsTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', email='admin@example.com', is_staff=True)
        self.client.force_authenticate(user=self.admin_user)

    def tearDown(self):
        remove_from_file('blacklist', 'newblackword')
        remove_from_file('whitelist', 'newwhiteword')

    def test_add_to_blacklist_view(self):
        url = reverse('management-add-to-blacklist')
        data = {'word': 'newblackword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with open('blog/utils/blacklists/blacklist.txt', 'r') as file:
            blacklist = file.read()
        self.assertIn('newblackword', blacklist)

    def test_remove_from_blacklist_view(self):
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
        url = reverse('management-add-to-whitelist')
        data = {'word': 'newwhiteword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with open('blog/utils/blacklists/whitelist.txt', 'r') as file:
            whitelist = file.read()
        self.assertIn('newwhiteword', whitelist)

    def test_remove_from_whitelist_view(self):
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
