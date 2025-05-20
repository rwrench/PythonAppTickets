import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from PythonApp1 import fetch_close_prices, calculate_ytd_change, format_result

class TestYTDChangeApp(unittest.TestCase):
    def test_calculate_ytd_change(self):
        close = pd.Series([100.0, 110.0, 120.0])
        latest_close, ytd_pct_change = calculate_ytd_change(close)
        self.assertEqual(latest_close, 120.0)
        self.assertAlmostEqual(ytd_pct_change, 20.0)

    def test_format_result_normal(self):
        result = format_result('MSFT', 120.0, 20.0)
        self.assertIn('MSFT', result)
        self.assertIn('120.00', result)
        self.assertIn('20.00%', result)

    def test_format_result_na(self):
        result = format_result('AAPL', None, None)
        self.assertIn('N/A', result)

    def test_format_result_error(self):
        result = format_result('MSTR', 'ERROR', None)
        self.assertIn('ERROR', result)

    @patch('PythonApp1.yf.download')
    def test_fetch_close_prices(self, mock_download):
        # Simulate a DataFrame with a 'Close' column as a Series
        df = pd.DataFrame({'Close': [100.0, 110.0, 120.0]})
        mock_download.return_value = df
        close = fetch_close_prices('MSFT', '2024-01-01', '2024-06-01')
        self.assertIsNotNone(close)
        self.assertEqual(list(close), [100.0, 110.0, 120.0])

    @patch('PythonApp1.yf.download')
    def test_fetch_close_prices_empty(self, mock_download):
        # Simulate an empty DataFrame
        mock_download.return_value = pd.DataFrame()
        close = fetch_close_prices('MSFT', '2024-01-01', '2024-06-01')
        self.assertIsNone(close)

if __name__ == '__main__':
    unittest.main()