import unittest
from datetime import datetime
from finance_utils import fetch_close_prices, calculate_ytd_change

class TestFinanceUtils(unittest.TestCase):
    def test_fetch_close_prices_valid(self):
        today = datetime.today().strftime('%Y-%m-%d')
        start_of_year = f'{datetime.today().year}-01-01'
        close = fetch_close_prices('MSFT', start_of_year, today)
        self.assertIsNotNone(close)
        self.assertGreater(len(close), 1)

    def test_fetch_close_prices_invalid(self):
        today = datetime.today().strftime('%Y-%m-%d')
        start_of_year = f'{datetime.today().year}-01-01'
        close = fetch_close_prices('INVALIDTICKER', start_of_year, today)
        self.assertIsNone(close)

    def test_calculate_ytd_change(self):
        import pandas as pd
        close = pd.Series([100, 120])
        latest_close, ytd_pct_change = calculate_ytd_change(close)
        self.assertEqual(latest_close, 120)
        self.assertAlmostEqual(ytd_pct_change, 20.0)

if __name__ == '__main__':
    unittest.main()