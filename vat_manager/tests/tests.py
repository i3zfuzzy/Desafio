from django.test import TestCase, Client
from django.urls import reverse


class TestExchangeRateView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_exchange_rate_data(self):
        response = self.client.get('/get_exchange_rate_data?start_date=2023-01-01&end_date=2023-01-05')
        self.assertEqual(response.status_code, 200)

    def test_table_view(self):
        response = self.client.get(reverse('table_view'))
        self.assertEqual(response.status_code, 200)
