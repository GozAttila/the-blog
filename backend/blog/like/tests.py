from blog.blogs.models import Blog
from blog.like.models import Like
from blog.like.views import LikeToggleView
from blog.like.serializers import LikeSerializer

from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

User = get_user_model()

class ModelsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.blog = Blog.objects.create(author=self.user, title='Test Blog', content='This is a test blog.', is_private=False)

    def test_like_creation(self):
        content_type = ContentType.objects.get_for_model(self.blog)
        like = Like.objects.create(user=self.user, content_type=content_type, object_id=self.blog.id, is_like=True)
        self.assertEqual(Like.objects.count(), 1)
        self.assertTrue(like.is_like)

class SerializersTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='serializeruser', email='serializer@example.com', password='password123')
        self.blog = Blog.objects.create(author=self.user, title='Serialized Blog', content='Serialized content', is_private=False)
        self.content_type = ContentType.objects.get_for_model(self.blog)
        self.like = Like.objects.create(user=self.user, content_type=self.content_type, object_id=self.blog.id, is_like=True)

    def test_like_serializer(self):
        serializer = LikeSerializer(instance=self.like)
        self.assertEqual(serializer.data['user'], self.user.id)
        self.assertEqual(serializer.data['is_like'], True)

class ViewsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', email='user1@example.com', password='password123')
        self.other_user = User.objects.create_user(username='user2', email='user2@example.com', password='password456')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.blog = Blog.objects.create(author=self.user, title='Test Blog', content='Content', is_private=False)
        self.content_type = ContentType.objects.get_for_model(self.blog)
        self.like_url = reverse('api-like-toggle', kwargs={
            'content_type': 'blog',
            'object_id': self.blog.id
        })

    def test_like_blog(self):
        response = self.client.post(self.like_url, {'is_like': True})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
        self.assertTrue(Like.objects.first().is_like)

    def test_dislike_blog(self):
        response = self.client.post(self.like_url, {'is_like': False})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
        self.assertFalse(Like.objects.first().is_like)

    def test_like_toggle(self):
        response = self.client.post(self.like_url, {'is_like': True})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

        response = self.client.post(self.like_url, {'is_like': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 0)

    def test_dislike_toggle(self):
        response = self.client.post(self.like_url, {'is_like': False})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

        response = self.client.post(self.like_url, {'is_like': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 0)

    def test_switch_reaction(self):
        self.client.post(self.like_url, {'is_like': True})
        response = self.client.post(self.like_url, {'is_like': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 1)
        self.assertFalse(Like.objects.first().is_like)

    def test_like_access_requires_authentication(self):
        self.client.credentials()
        response = self.client.post(self.like_url, {'is_like': True})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class URLsTests(APITestCase):
    def test_like_url_resolves(self):
        url = reverse('api-like-toggle', kwargs={'content_type': 'blog', 'object_id': 1})
        self.assertEqual(resolve(url).func.view_class, LikeToggleView)
