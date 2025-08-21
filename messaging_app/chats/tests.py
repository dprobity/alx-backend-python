from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

class UserRegistrationTestCase(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpassword",
            "confirm_password": "testpassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(get_user_model().objects.filter(email="testuser@example.com").exists())


class JWTLoginTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="loginuser@example.com",
            password="password123",
            first_name="Login",
            last_name="User"
        )

    def test_jwt_login(self):
        url = reverse('jwt_login')
        data = {
            "email": "loginuser@example.com",
            "password": "password123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
