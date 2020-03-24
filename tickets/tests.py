from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from accounts.models import Account


class APICreateTicket(APITestCase):
    def setUp(self):
        self.test_user = Account.objects.create_user('user@example.com', 'userpassword')
        self.customer_service_user = Account.objects.create_user('support@example.com', 'supportpassword')
        self.customer_service_user.is_customer_service = True
        self.customer_service_user.save()
        self.new_ticket_url = reverse('new_ticket')
        Token.objects.create(user=self.test_user)
        Token.objects.create(user=self.customer_service_user)

    def test_create_new_ticket_success(self):
        data = {
            "subject": "subject",
            "description": "description"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user.auth_token.key)
        response = self.client.post(self.new_ticket_url, data, format='json')
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['result']['subject'], data['subject'])

    def test_create_new_ticket_with_failed_auth(self):
        data = {
            "subject": "subject",
            "description": "description"
        }

        response = self.client.post(self.new_ticket_url, data, format='json')
        self.assertEqual(response.data['status_code'], status.HTTP_401_UNAUTHORIZED)

    def test_create_new_ticket_from_customer_service(self):
        data = {
            "subject": "subject",
            "description": "description"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_service_user.auth_token.key)
        response = self.client.post(self.new_ticket_url, data, format='json')
        self.assertEqual(response.data['result']['error'], 'You are not allowed to create a ticket. ')

    def test_create_new_ticket_with_no_subject(self):
        data = {
            "subject": "",
            "description": "message"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.test_user.auth_token.key)
        response = self.client.post(self.new_ticket_url, data, format='json')
        self.assertEqual(response.data['result']['subject'], [ErrorDetail(string='This field may not be blank.', code='blank')])

    def test_create_new_ticket_with_no_description(self):
        data = {
            "subject": "subject",
            "description": ""
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.test_user.auth_token.key)
        response = self.client.post(self.new_ticket_url, data, format='json')
        self.assertEqual(response.data['result']['description'], [ErrorDetail(string='This field may not be blank.', code='blank')])
