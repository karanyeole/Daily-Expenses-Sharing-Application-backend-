# expenses_app/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class UserTests(APITestCase):
    def test_create_user(self):
        url = reverse('create_user')
        data = {'email': 'test@example.com', 'name': 'Test User', 'mobile': '1234567890'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        user = User.objects.create_user(username='test@example.com', password='testpassword')
        url = reverse('user_login')
        data = {'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
