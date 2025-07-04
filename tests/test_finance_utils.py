import unittest
import sys
import os

# Add the api_app directory to the path so we can import finance_utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api_app'))

try:
    from finance_utils import fetch_close_prices, calculate_ytd_change
    FINANCE_UTILS_AVAILABLE = True
except ImportError:
    FINANCE_UTILS_AVAILABLE = False

class TestFinanceUtils(unittest.TestCase):
    
    def test_imports(self):
        """Test that we can import required modules"""
        import yfinance
        import pandas
        self.assertTrue(True)
    
    @unittest.skipUnless(FINANCE_UTILS_AVAILABLE, "finance_utils not available")
    def test_calculate_ytd_change(self):
        """Test YTD calculation with mock data"""
        # Test with mock data
        current_price = 150.0
        ytd_start_price = 100.0
        
        result = calculate_ytd_change(current_price, ytd_start_price)
        
        # Should return a dictionary with percentage and dollar change
        self.assertIsInstance(result, dict)
        self.assertIn('ytd_change_percent', result)
        self.assertIn('ytd_change_dollar', result)
        
        # Verify calculation: (150-100)/100 * 100 = 50%
        self.assertEqual(result['ytd_change_percent'], 50.0)
        self.assertEqual(result['ytd_change_dollar'], 50.0)
    
    def test_simple_webapp_imports(self):
        """Test that simple_fresh_webapp can be imported"""
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        try:
            import simple_fresh_webapp
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Could not import simple_fresh_webapp: {e}")

class TestBasicFunctionality(unittest.TestCase):
    def test_python_version(self):
        """Test that we're running Python 3.11+"""
        self.assertGreaterEqual(sys.version_info[:2], (3, 11))
    
    def test_required_packages(self):
        """Test that required packages are available"""
        try:
            import flask
            import yfinance
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Required package not available: {e}")

if __name__ == '__main__':
    unittest.main()