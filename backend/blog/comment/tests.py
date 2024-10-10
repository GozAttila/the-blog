from blog.blogs.models import Blog, Invitation

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

User = get_user_model()

class CommentTests(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='author', password='password', email='author@example.com')
        self.invited_user = User.objects.create_user(username='invited', password='password', email='invited@example.com')
        self.non_invited_user = User.objects.create_user(username='non_invited', password='password', email='noninvited@example.com')

        self.author_token = Token.objects.create(user=self.author)
        self.invited_user_token = Token.objects.create(user=self.invited_user)
        self.non_invited_user_token = Token.objects.create(user=self.non_invited_user)

        self.private_blog = Blog.objects.create(author=self.author, title='Private Blog', content='Content', is_private=True)

        self.invitation = Invitation.objects.create(blog=self.private_blog, invited_user=self.invited_user, invited_by=self.author, is_accepted=True)

        self.comment_create_url = reverse('api-comment-create', kwargs={'blog_id': self.private_blog.id})
        self.comment_list_url = reverse('api-comment-list', kwargs={'blog_id': self.private_blog.id})

    def api_authentication(self, user_token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)

    def test_author_can_comment_on_own_private_blog(self):
        self.api_authentication(self.author_token)
        response = self.client.post(self.comment_create_url, {'content': 'Author comment'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invited_user_can_comment_on_private_blog(self):
        self.api_authentication(self.invited_user_token)
        response = self.client.post(self.comment_create_url, {'content': 'Invited user comment'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_non_invited_user_cannot_comment_on_private_blog(self):
        self.api_authentication(self.non_invited_user_token)
        response = self.client.post(self.comment_create_url, {'content': 'Non-invited user comment'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invited_user_can_view_comments_on_private_blog(self):
        self.api_authentication(self.invited_user_token)
        response = self.client.get(self.comment_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_invited_user_cannot_view_comments_on_private_blog(self):
        self.api_authentication(self.non_invited_user_token)
        response = self.client.get(self.comment_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unauthenticated_user_cannot_create_comment(self):
        response = self.client.post(self.comment_create_url, {'content': 'Unauthenticated user comment'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_view_comments(self):
        response = self.client.get(self.comment_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
