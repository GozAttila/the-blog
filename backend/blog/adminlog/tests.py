from blog.adminlog.models import AdminLog, AdminMessage
from blog.adminlog.serializers import AdminMessageSerializer
from blog.adminlog.views import AdminMessageCreateView, AdminMessageListView

from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from rest_framework.test import APIRequestFactory

User = get_user_model()

class ModelsTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', email='admin@example.com', is_staff=True)
        self.user = User.objects.create_user(username='user', password='userpass', email='user@example.com')
        self.content_type = ContentType.objects.get_for_model(User)

    def test_adminlog_creation(self):
        log_entry = AdminLog.objects.create(
            admin=self.admin_user,
            action_type="BLOCK",
            content_type=self.content_type,
            object_id=self.user.id,
            description="User blocked"
        )
        self.assertEqual(AdminLog.objects.count(), 1)
        self.assertEqual(log_entry.action_type, "BLOCK")

class SerializersTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', email='admin@example.com', is_staff=True)
        self.user = User.objects.create_user(username='user', password='userpass', email='user@example.com')

    def test_adminmessage_serializer(self):
        data = {
            'sender': self.admin_user.id,
            'recipient': self.user.id,
            'subject': 'Test Subject',
            'body': 'Test Body',
        }
        request = self.client.request().wsgi_request
        request.user = self.admin_user
        serializer = AdminMessageSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())
        message = serializer.save()
        self.assertEqual(message.subject, 'Test Subject')
        self.assertEqual(message.body, 'Test Body')

class ViewsTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', email='admin@example.com', is_staff=True)
        self.user = User.objects.create_user(username='user', password='userpass', email='user@example.com')
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.user_token = Token.objects.create(user=self.user)

        self.message_url = reverse('admin-message-send')
        self.list_url = reverse('admin-message-list')

    def api_authentication(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_admin_sends_message(self):
        self.api_authentication(self.admin_token)
        response = self.client.post(self.message_url, {
            'recipient': self.user.id,
            'subject': 'Test Subject',
            'body': 'Test Body'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AdminMessage.objects.count(), 1)

    def test_user_cannot_send_message(self):
        self.api_authentication(self.user_token)
        response = self.client.post(self.message_url, {
            'recipient': self.admin_user.id,
            'subject': 'Test Subject',
            'body': 'Test Body'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_message_list_for_user(self):
        AdminMessage.objects.create(
            sender=self.admin_user,
            recipient=self.user,
            subject="Message 1",
            body="This is message 1"
        )
        self.api_authentication(self.user_token)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class URLsTests(APITestCase):
    def test_admin_message_send_url(self):
        url = reverse('admin-message-send')
        self.assertEqual(resolve(url).func.view_class, AdminMessageCreateView)

    def test_admin_message_list_url(self):
        url = reverse('admin-message-list')
        self.assertEqual(resolve(url).func.view_class, AdminMessageListView)
