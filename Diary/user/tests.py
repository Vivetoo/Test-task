from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch, MagicMock

from user.models import CustomUser
from .token import get_token



class UserTestCase(APITestCase):



    def test_create_user(self):
        data = {
            'email': 'mail@mail.ru',
            'first_name': 'Дмитрий',
            'second_name': 'Салаткин',
            'last_name': 'Викторович',
            'password': '123',
            'password2': '123',
        }
        response = self.client.post('/api/v1/user/register/', data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('user.views.StudentLoginAPIView.post')
    def test_login(self, mock_user):
        mock_user.return_value = {
            'email': 'mail@mail.ru',
            'first_name': 'Дмитрий',
            'second_name': 'Салаткин',
            'last_name': 'Викторович',
            'password': '123',
            'password2': '123',
        }
        data = {
            'email': 'mail@mail.ru',
            'password': '123',
        }
        client = APIClient()
        response = self.client.post(reverse('login'), data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile(self):
        user = CustomUser.objects.create(
            email='mail@mail.ru',
            first_name='fddewfdw',
            second_name='ewfew',
            last_name='ewfewf',
            password='123',
        )
        data = {'Bearer': ''}
        response = self.client.post('/api/v1/user/profile/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

