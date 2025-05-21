import sys
import os
import unittest
import pandas as pd

# Add parent directory to sys.path so PythonApp1 can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PythonApp1 import calculate_ytd_change, format_result

class TestPythonApp1(unittest.TestCase):
    def test_calculate_ytd_change(self):
        close = pd.Series([100, 110])
        latest_close, ytd_pct_change = calculate_ytd_change(close)
        self.assertEqual(latest_close, 110)
        self.assertAlmostEqual(ytd_pct_change, 10.0)

    def test_format_result_none(self):
        result = format_result("MSFT", None, None)
        self.assertIn("N/A", result)

    def test_format_result_error(self):
        result = format_result("MSFT", "ERROR", None)
        self.assertIn("ERROR", result)

    def test_format_result_normal(self):
        result = format_result("MSFT", 110, 10.0)
        self.assertIn("MSFT", result)
        self.assertIn("110.00", result)
        self.assertIn("10.00%", result)

if __name__ == "__main__":
    unittest.main()