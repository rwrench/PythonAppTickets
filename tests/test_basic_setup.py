import unittest
import sys
import os

class TestBasicSetup(unittest.TestCase):
    """Basic tests that don't require external APIs"""
    
    def test_python_version(self):
        """Test that we're running Python 3.11+"""
        self.assertGreaterEqual(sys.version_info[:2], (3, 11))
    
    def test_required_packages_import(self):
        """Test that required packages can be imported"""
        try:
            import flask
            import yfinance
            import pandas
            self.assertTrue(True, "All required packages imported successfully")
        except ImportError as e:
            self.fail(f"Required package not available: {e}")
    
    def test_simple_webapp_exists(self):
        """Test that simple_fresh_webapp.py exists and is readable"""
        webapp_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'simple_fresh_webapp.py')
        self.assertTrue(os.path.exists(webapp_path), "simple_fresh_webapp.py should exist")
        self.assertTrue(os.path.isfile(webapp_path), "simple_fresh_webapp.py should be a file")
    
    def test_api_files_exist(self):
        """Test that API files exist"""
        api_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'api_app')
        api_server = os.path.join(api_dir, 'api_server.py')
        finance_utils = os.path.join(api_dir, 'finance_utils.py')
        
        self.assertTrue(os.path.exists(api_server), "api_server.py should exist")
        self.assertTrue(os.path.exists(finance_utils), "finance_utils.py should exist")
    
    def test_web_app_files_exist(self):
        """Test that web app files exist"""
        web_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'web_app')
        web_app = os.path.join(web_dir, 'web_app.py')
        
        self.assertTrue(os.path.exists(web_app), "web_app.py should exist")

if __name__ == '__main__':
    unittest.main()
