from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from .models import Account


class APIAccountsTest(APITestCase):
    def setUp(self):
        self.test_user = Account.objects.create_user('test_user@example.com', 'test_userpassword')

        self.account_create_url = reverse('account_create')
        self.api_token_auth_url = reverse('api_token_auth')

    def test_create_user_success(self):
        data = {
            'email': 'user1@example.com',
            'password': 'user1password'
        }

        response = self.client.post(self.account_create_url, data, format='json')
        account = Account.objects.latest('id')
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], data['email'])

    def test_create_user_with_no_password(self):
        data = {
            'email': 'user2@example.com',
            'password': ''
        }

        response = self.client.post(self.account_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(response.data['status_code'], status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_no_email(self):
        data = {
            'email': '',
            'password': 'user3password'
        }

        response = self.client.post(
            self.account_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(response.data['status_code'], status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_invalid_email(self):
        data = {
            'email':  'testing',
            'passsword': 'password'
        }

        response = self.client.post(
            self.account_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(response.data['status_code'], status.HTTP_400_BAD_REQUEST)

    def test_get_token_success(self):
        data = {
            'username': 'test_user@example.com',
            'password': 'test_userpassword'
        }

        response = self.client.post(
            self.api_token_auth_url, data, format='json')
        user = Account.objects.get(email='test_user@example.com')
        token = Token.objects.get(user=user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], token.key)

    def test_get_token_fail(self):
        data = {
            'email': 'test_user@example.com',
            'password': 'password'
        }

        response = self.client.post(self.api_token_auth_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
