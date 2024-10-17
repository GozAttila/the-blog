from blog.user.models import User
from blog.user.serializers import UserRegistrationSerializer
from blog.user.views import register_user, CustomAuthToken

from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class ModelsTests(APITestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username='user1', password='password', email='user1@example.com')
        self.assertEqual(user.username, 'user1')
        self.assertEqual(user.email, 'user1@example.com')
        self.assertTrue(user.check_password('password'))

class SerializersTests(APITestCase):
    def test_user_registration_serializer(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')

    def test_username_validation(self):
        User.objects.create_user(
            username='existinguser', 
            email='existing@example.com', 
            password='password123'
        )
        data = {
            'username': 'existinguser', 
            'email': 'newuser@example.com', 
            'password': 'password123'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

        data = {
            'username': 'neutralname',
            'email': 'neutral@example.com',
            'password': 'password123'
        }
        self.assertTrue(UserRegistrationSerializer(data=data).is_valid())

        data = {
            'username': 'testforwhite',
            'email': 'white@example.com',
            'password': 'password123'
        }
        self.assertTrue(UserRegistrationSerializer(data=data).is_valid())

        data = {
            'username': 'testforblack',
            'email': 'black@example.com',
            'password': 'password123'
        }
        self.assertFalse(UserRegistrationSerializer(data=data).is_valid())

        data = {
            'username': 'testforgrey',
            'email': 'grey@example.com',
            'password': 'password123'
        }
        self.assertTrue(UserRegistrationSerializer(data=data).is_valid())

    def test_email_validation(self):
        User.objects.create_user(
            username='newuser2', 
            email='existingemail@example.com', 
            password='password123'
        )
        data = {
            'username': 'newuser', 
            'email': 'existingemail@example.com', 
            'password': 'password123'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

class ViewsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client = self.client_class()
        self.token = Token.objects.create(user=self.user)

    def test_register_user(self):
        url = reverse('api-register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        url = reverse('api-login')
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_username_validation_api(self):
        url = reverse('api-register')

        valid_data = {
            'username': 'neutralname',
            'email': 'neutral@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        valid_data = {
            'username': 'testforwhite',
            'email': 'white@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        invalid_data = {
            'username': 'testforblack',
            'email': 'black@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        valid_data = {
            'username': 'testforgrey',
            'email': 'grey@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class URLsTests(APITestCase):
    def test_register_url(self):
        url = reverse('api-register')
        self.assertEqual(resolve(url).func, register_user)

    def test_login_url(self):
        url = reverse('api-login')
        self.assertEqual(resolve(url).func.view_class, CustomAuthToken)
