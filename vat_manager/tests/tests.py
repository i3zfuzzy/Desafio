import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock
import asyncio

from asgiref.sync import sync_to_async

from vat_manager.views import get_datas_between_period, date_range, fetch_and_save_exchange_rates, \
    get_exchange_rate_data, TableView


class TestYourFunctions(unittest.TestCase):

    def test_get_datas_between_period(self):
        start_date = "2023-10-20"
        end_date = "2023-10-25"
        expected_dates = [datetime(2023, 10, 20), datetime(2023, 10, 21), datetime(2023, 10, 22),
                          datetime(2023, 10, 23), datetime(2023, 10, 24), datetime(2023, 10, 25)]
        self.assertEqual(get_datas_between_period(start_date, end_date), expected_dates)

    def test_date_range(self):
        date_s = "2023-10-20"
        date_e = "2023-10-25"
        self.assertTrue(date_range(date_s, date_e))

    @sync_to_async
    def test_fetch_and_save_exchange_rates(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(fetch_and_save_exchange_rates("2023-10-20", "2023-10-25"))

    def test_get_exchange_rate_data(self):
        mock_request = MagicMock()
        mock_request.GET.get.return_value = '2023-10-20'
        # Add more mock attributes as needed

        response = get_exchange_rate_data(mock_request)

    def test_table_view(self):
        mock_request = MagicMock()

        response = TableView().get(mock_request)


if __name__ == '__main__':
    unittest.main()