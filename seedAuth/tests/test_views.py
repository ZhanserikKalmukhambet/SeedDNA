from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework.test import APIClient


class TestRegisterView(TestCase):
    def test_registration_success(self):
        data = {'email': 'test@gmail.com',
                'name': 'test',
                'surname': 'test',
                'password': 'test'
        }

        response = self.client.post(reverse('sign_up'), data=data, format='json')

        self.assertEquals(response.status_code, 201)


class TestLoginView(TestCase):
    def test_login_success(self):
        client = APIClient()

        data = {
            'email': 'test@gmail.com',
            'password': 'test'
        }

        response = client.post(reverse('token_obtain_pair'), data=data, format='json')
        self.assertEquals(response.status_code, 401)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)