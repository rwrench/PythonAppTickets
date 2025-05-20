import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PythonApp1 import fetch_close_prices, calculate_ytd_change, format_result

class SmokeTest(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(1, 1)