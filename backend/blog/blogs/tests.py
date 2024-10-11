from blog.blogs.models import Blog, Invitation, BlogTranslation
from blog.blogs.serializers import BlogSerializer
from blog.blogs.views import BlogDetailView

from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

class ModelsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.blog = Blog.objects.create(author=self.user, title='Test Blog', content='This is a test blog.', is_private=True)

    def test_blog_creation(self):
        self.assertEqual(Blog.objects.count(), 1)
        self.assertEqual(self.blog.title, 'Test Blog')
        self.assertTrue(self.blog.is_private)

    def test_blog_translation_creation(self):
        translation = BlogTranslation.objects.create(
            blog=self.blog,
            language='es',
            translated_title='Prueba de Blog',
            translated_content='Este es un blog de prueba.'
        )
        self.assertEqual(BlogTranslation.objects.count(), 1)
        self.assertEqual(translation.translated_title, 'Prueba de Blog')
        self.assertEqual(translation.language, 'es')

class SerializersTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='serializeruser', email='serializer@example.com', password='password123')
        self.blog = Blog.objects.create(author=self.user, title='Serialized Blog', content='Serialized content', is_private=False)

    def test_blog_serializer(self):
        serializer = BlogSerializer(instance=self.blog)
        self.assertEqual(serializer.data['title'], 'Serialized Blog')
        self.assertEqual(serializer.data['content'], 'Serialized content')
        self.assertEqual(serializer.data['author'], self.user.id)

class ViewsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', email='user1@example.com', password='password123')
        self.other_user = User.objects.create_user(username='user2', email='user2@example.com', password='password456')
        self.invited_user = User.objects.create_user(username='inviteduser', email='invited@example.com', password='password789')
        self.user_token = Token.objects.create(user=self.user)
        self.invited_user_token = Token.objects.create(user=self.invited_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        
        self.blog = Blog.objects.create(author=self.user, title='Test Blog', content='Content', is_private=True)
        self.invitation = Invitation.objects.create(blog=self.blog, invited_user=self.invited_user, invited_by=self.user)
        self.blog_create_url = reverse('api-blog-list')
        self.blog_detail_url = reverse('api-blog-detail', args=[self.blog.id])
        self.translation_url = reverse('api-blog-translation', args=[self.blog.id])

    def test_create_public_blog(self):
        data = {'title': 'New Public Blog', 'content': 'Public content', 'is_private': False}
        response = self.client.post(self.blog_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blog.objects.count(), 2)

    def test_edit_blog_content(self):
        response = self.client.patch(self.blog_detail_url, {'content': 'Updated content'})
        self.blog.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.blog.content, 'Updated content')

    def test_delete_blog(self):
        response = self.client.delete(self.blog_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Blog.objects.filter(id=self.blog.id).exists())

    def test_private_blog_access_by_invited_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.invited_user_token.key)
        self.client.post(reverse('api-invitation-accept', args=[self.invitation.id]), {'is_accepted': True})
        response = self.client.get(self.blog_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_private_blog_access_denied_for_non_invited_user(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.blog_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_blog_translation(self):
        response = self.client.post(self.translation_url, {
            'language': 'de',
            'translated_title': 'Blog-Test',
            'translated_content': 'Dies ist ein Testblog.'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogTranslation.objects.count(), 1)

class URLsTests(APITestCase):
    def test_blog_detail_url(self):
        url = reverse('api-blog-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, BlogDetailView)
