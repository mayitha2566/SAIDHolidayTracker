from django.test import TestCase, Client
from django.urls import reverse
from .models import SAID, Holiday
from .views import is_valid_id_number
from django.conf import settings
from unittest import mock

class IsValidIDNumberTest(TestCase):
    def test_valid_id_number(self):
        self.assertTrue(is_valid_id_number('8001015009087'))

    def test_invalid_id_number_length(self):
        self.assertFalse(is_valid_id_number('80010150090'))

    def test_invalid_id_number_non_digit(self):
        self.assertFalse(is_valid_id_number('80010150090AB'))

    def test_invalid_id_number_checksum(self):
        self.assertFalse(is_valid_id_number('8001015009086'))

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'system_management/home.html')

    def test_post_valid_id(self):
        with mock.patch('requests.get') as mocked_get:
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.json.return_value = {
                'meta': {'code': 200},
                'response': {
                    'holidays': []
                }
            }
            response = self.client.post(self.url, {'id_number': '8001015009087'})
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'system_management/results.html')
            self.assertContains(response, 'SAID')

    def test_post_invalid_id(self):
        response = self.client.post(self.url, {'id_number': '1234567890123'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'system_management/results.html')
        self.assertContains(response, 'Invalid South African ID number.')

    def test_post_invalid_date(self):
        response = self.client.post(self.url, {'id_number': '9902305009087'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'system_management/results.html')
        self.assertContains(response, 'Invalid date in ID number.')

    def test_post_api_error(self):
        with mock.patch('requests.get') as mocked_get:
            mocked_get.return_value.status_code = 500
            response = self.client.post(self.url, {'id_number': '8001015009087'})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Error fetching holidays from API.')

    def test_post_network_error(self):
        with mock.patch('requests.get', side_effect=Exception('Network error')):
            response = self.client.post(self.url, {'id_number': '8001015009087'})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Network error occurred while fetching holidays.')