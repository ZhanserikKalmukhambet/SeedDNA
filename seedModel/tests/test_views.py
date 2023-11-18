import json

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from seedAuth.models import UserData


class TestViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.pred_model_url = reverse('predict_model')
        self.input_path = 'C:\\Users\\User\\Downloads\\input.jpg'

    def test_predict_model_POST(self):
        # Assuming I have authentication set up for your view
        user_credentials = {
            'email': 'qazaq@gmail.com',
            'name': 'qazaq',
            'surname': 'qazaq',
            'password': 'qazaq'
        }

        test_user = UserData.objects.create(**user_credentials)
        self.client.force_authenticate(user=test_user)

        with open(self.input_path, 'rb') as img_file:
            response = self.client.post(self.pred_model_url, {'image': img_file}, format='multipart')

        # Check if the response status code is as expected (e.g., 200)
        self.assertEquals(response.status_code, 200)

        # Parse the JSON response and make assertions based on view's behavior
        response_data = json.loads(response.content)
        self.assertIn('file_url', response_data)
        self.assertIn('percent', response_data)
        self.assertIn('fragments', response_data)
        self.assertIn('fragmented_degradeds', response_data)
        self.assertIn('normals', response_data)


