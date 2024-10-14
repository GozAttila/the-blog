from blog.report.models import Report
from blog.blogs.models import Blog
from blog.report.views import ReportActionView, ReportCreateView

from django.urls import resolve, reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

User = get_user_model()

class ModelsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='userpass', email='user@example.com')
        self.blog = Blog.objects.create(author=self.user, title='Test Blog', content='This is a test blog.')

    def test_report_creation(self):
        content_type = ContentType.objects.get_for_model(self.blog)
        report = Report.objects.create(reported_by=self.user, content_type=content_type, object_id=self.blog.id, reason='Inappropriate content')
        self.assertEqual(report.reason, 'Inappropriate content')
        self.assertEqual(report.reported_by, self.user)

class SerializersTests(APITestCase):
    def test_report_serializer(self):
        user = User.objects.create_user(username='user2', password='password', email='user2@example.com')
        content_type = ContentType.objects.get_for_model(Blog)
        report = Report.objects.create(reported_by=user, content_type=content_type, object_id=1, reason='Inappropriate content')
        from blog.report.serializers import ReportSerializer
        serializer = ReportSerializer(report)
        data = serializer.data
        self.assertEqual(data['reason'], 'Inappropriate content')

class ViewsTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', email='admin@example.com', is_staff=True)
        self.user = User.objects.create_user(username='user', password='userpass', email='user@example.com')
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.user_token = Token.objects.create(user=self.user)
        self.blog = Blog.objects.create(author=self.user, title='Test Blog', content='This is a test blog.')

        self.blog_content_type = ContentType.objects.get_for_model(Blog)

        self.report_create_url = reverse('api-report-create', args=['blog', self.blog.id])
        self.report_action_url = lambda report_id: reverse('report-action', args=[report_id])

    def api_authentication(self, user_token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)

    def test_user_can_create_report(self):
        self.api_authentication(self.user_token)
        response = self.client.post(self.report_create_url, {'reason': 'Inappropriate content'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Report.objects.count(), 1)

    def test_admin_can_block_content(self):
        self.api_authentication(self.admin_token)
        report = Report.objects.create(reported_by=self.user, content_type=self.blog_content_type, object_id=self.blog.id, reason='Inappropriate content')
        response = self.client.post(self.report_action_url(report.id), {'action': 'block'})
        self.blog.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.blog.is_blocked)

    def test_other_admin_cannot_block_already_blocked_content(self):
        self.api_authentication(self.admin_token)
        self.blog.is_blocked = True
        self.blog.save()
        report = Report.objects.create(reported_by=self.user, content_type=self.blog_content_type, object_id=self.blog.id, reason='Inappropriate content')
        response = self.client.post(self.report_action_url(report.id), {'action': 'block'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_unblock_content(self):
        self.api_authentication(self.admin_token)
        self.blog.is_blocked = True
        self.blog.save()
        report = Report.objects.create(reported_by=self.user, content_type=self.blog_content_type, object_id=self.blog.id, reason='Inappropriate content')
        response = self.client.post(self.report_action_url(report.id), {'action': 'unblock'})
        self.blog.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.blog.is_blocked)

class URLsTests(APITestCase):
    def test_report_create_url(self):
        url = reverse('api-report-create', args=['blog', 1])
        self.assertEqual(resolve(url).func.view_class, ReportCreateView)

    def test_report_action_url(self):
        url = reverse('report-action', args=[1])
        self.assertEqual(resolve(url).func.view_class, ReportActionView)
