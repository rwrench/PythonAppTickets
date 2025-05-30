from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import pytest


def get_driver():
    options = Options()
    options.add_argument("--headless")  # For CI or headless testing
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Automatically downloads and uses the correct ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://pythonappticketsweb.onrender.com/")
    return driver

def wait_for_element(driver, locator, ec, timeout=20):
    """Wait for an element matching the locator and expected condition."""
    return WebDriverWait(driver, timeout).until(
        ec(locator)
    )

def click_button(driver, ticker_input, ticker_txt):
    analyze_btn = driver.find_element(By.ID, "analyze-btn")
    ticker_input.clear()
    ticker_input.send_keys(ticker_txt)
    analyze_btn.click()
    print(f"Clicked button with tickers: {ticker_txt}")
    return analyze_btn
    

def get_visible_results(driver):
    results = wait_for_element(driver,
        (By.TAG_NAME, "pre"), 
        EC.visibility_of_element_located, timeout=30).text
    print("RESULTS:", results)
    return results

 
def test_valid_tickers_display_ytd():
    print("Starting test for valid tickers display...")
    driver = get_driver()
    try:
        ticker_input = wait_for_element(driver,
            (By.NAME, "tickers"), 
           EC.presence_of_element_located, timeout=60)
        click_button(driver, ticker_input, "MSFT,AAPL") 
        results = get_visible_results(driver)
        assert "MSFT" in results
        assert "AAPL" in results
        print("Valid tickers display test passed.")
    except Exception as e:
        print("Test failed:", e)
        print(driver.page_source)  # Add this line
        raise
    finally:
        driver.quit()

def test_invalid_ticker_reported():
    print("Starting test for invalid ticker reporting...")
    driver = get_driver()
    try:
        ticker_input = wait_for_element(driver,
            (By.NAME, "tickers"), 
            EC.presence_of_element_located, timeout=60)
        
        click_button(driver, ticker_input, "INVALID")
        results = get_visible_results(driver)
        assert "No valid tickers found. Please enter valid stock symbols." in results or "INVALID" in results
        print("Invalid ticker reporting test passed.")
    except Exception as e:
        print("Test failed:", e)
        print(driver.page_source)  # Add this line
        raise
    finally:
        driver.quit()
   

@pytest.mark.skip(reason="Spinner may not be visible if backend is fast; skipping in CI.")
def test_spinner_and_button_disabled():
    print("Starting test for spinner and button state after submit...")
    driver = get_driver()
    try:
        ticker_input = wait_for_element(driver,
            (By.NAME, "tickers"), 
            EC.presence_of_element_located, timeout=60)
        
        analyze_btn = click_button(driver, ticker_input, "MSFT,AAPL") 

        spinner = wait_for_element(driver,
            (By.ID, "spinner"),
            EC.visibility_of_element_located, timeout=30)
        assert spinner.is_displayed(), "Spinner should be visible after submit"
        WebDriverWait(driver, 10).until(
            lambda d: analyze_btn.get_attribute("disabled") == "true"
        )
        assert analyze_btn.get_attribute("disabled") == "true", "Button should be disabled after submit"
        print("Spinner and button state test passed.")
    except Exception as e:
        print("Test failed:", e)
        print(driver.page_source) 
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Running Selenium tests...")  
    test_valid_tickers_display_ytd()
    test_invalid_ticker_reported()
    test_spinner_and_button_disabled()
    print("All tests completed.")