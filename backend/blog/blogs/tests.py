from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from blog.blogs.models import Blog, Invitation, BlogTranslation
from blog.user.models import User

class BlogTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', email='other@example.com', password='password456')
        self.admin = User.objects.create_user(username='adminuser', email='admin@example.com', password='adminpassword')
        self.admin.is_staff = True
        self.admin.save()
        self.blog = Blog.objects.create(author=self.user, title='Test Blog', content='This is a test blog.', is_private=True)
        self.invitation = Invitation.objects.create(blog=self.blog, invited_user=self.other_user, invited_by=self.user)

    def test_blog_creation(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api-blog-list')
        response = self.client.post(url, {'title': 'New Blog', 'content': 'Blog content', 'is_private': False})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blog.objects.count(), 2)

    def test_private_blog_access(self):
        # Not invited user should not access the blog
        self.client.force_authenticate(user=self.other_user)
        url = reverse('api-blog-detail', args=[self.blog.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Invited user accepts invitation and should access the blog
        invitation_url = reverse('api-invitation-accept', args=[self.invitation.id])
        self.client.post(invitation_url, {'is_accepted': True})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_blog_editing(self):
        # Blog author edits their blog
        self.client.force_authenticate(user=self.user)
        url = reverse('api-blog-detail', args=[self.blog.id])
        response = self.client.patch(url, {'content': 'Updated content'})
        self.blog.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.blog.content, 'Updated content')

    def test_blog_deletion_by_author(self):
        # Blog author deletes their blog
        self.client.force_authenticate(user=self.user)
        url = reverse('api-blog-detail', args=[self.blog.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Blog.objects.filter(id=self.blog.id).exists())

    def test_blocked_blog_visibility(self):
        # Admin blocks the blog
        self.client.force_authenticate(user=self.admin)
        report_url = reverse('api-report-create', args=['blog', self.blog.id])
        self.client.post(report_url, {'reason': 'Spam', 'report_type': 'Abuse'})
        action_url = reverse('report-action', args=[self.blog.id])
        block_response = self.client.post(action_url, {'action': 'block'})
        self.blog.refresh_from_db()
        self.assertEqual(block_response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.blog.is_blocked)

        # Blog author should still see their blocked blog
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('api-blog-detail', args=[self.blog.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Other users should not see the blocked blog
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(reverse('api-blog-detail', args=[self.blog.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_blog_translation(self):
        # Blog author adds a translation
        self.client.force_authenticate(user=self.user)
        translation_url = reverse('api-blog-translation', args=[self.blog.id])
        response = self.client.post(translation_url, {'language': 'es', 'translated_title': 'Prueba de Blog', 'translated_content': 'Este es un blog de prueba.'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogTranslation.objects.count(), 1)
        translation = BlogTranslation.objects.first()
        self.assertEqual(translation.translated_title, 'Prueba de Blog')
        self.assertEqual(translation.translated_content, 'Este es un blog de prueba.')
