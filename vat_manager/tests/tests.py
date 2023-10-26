from datetime import datetime, timedelta
from django.test import TestCase
from .models import ExchangeRate
from .views import get_datas_between_period, date_range, fetch_and_save_exchange_rates


class TestGetDatasBetweenPeriod(TestCase):
    def test_get_datas_between_period(self):
        date_i = "2023-01-01"
        date_e = "2023-01-05"
        expected_dates = [datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3), datetime(2023, 1, 4),
                          datetime(2023, 1, 5)]
        result = get_datas_between_period(date_i, date_e)
        self.assertEqual(result, expected_dates)


class TestDateRange(TestCase):
    def test_date_range(self):
        date_s = "2023-01-01"
        date_e = "2023-01-05"
        result = date_range(date_s, date_e)
        self.assertTrue(result)


class TestFetchAndSaveExchangeRates(TestCase):
    def test_fetch_and_save_exchange_rates(self):
        start_date = "2023-01-01"
        end_date = "2023-01-05"
        fetch_and_save_exchange_rates(start_date, end_date)
        result = ExchangeRate.objects.filter(date__gte=start_date, date__lte=end_date).exists()
        self.assertTrue(result)
