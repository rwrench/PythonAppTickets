from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import os


def get_driver():
    driver_path = os.path.join(os.path.dirname(__file__), "chromedriver.exe")
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get("https://pythonappticketsweb.onrender.com/")
    return driver

def test_spinner_and_button_disabled():
    driver = get_driver()
    ticker_input = driver.find_element(By.NAME, "tickers")
    analyze_btn = driver.find_element(By.ID, "analyze-btn")
    ticker_input.clear()
    ticker_input.send_keys("MSFT,AAPL,INVALID")
    analyze_btn.click()
    time.sleep(0.5)
    spinner = driver.find_element(By.ID, "spinner")
    assert spinner.is_displayed(), "Spinner should be visible after submit"
    assert analyze_btn.get_attribute("disabled") == "true", "Button should be disabled after submit"
    print("Spinner and button state test passed.")
    driver.quit()

def test_valid_tickers_display_ytd():
    print("Starting test for valid tickers display...")
    driver = get_driver()
    ticker_input = driver.find_element(By.NAME, "tickers")
    analyze_btn = driver.find_element(By.ID, "analyze-btn")
    ticker_input.clear()
    ticker_input.send_keys("MSFT,AAPL")
    analyze_btn.click()
    print("Button clicked, waiting for results...")
    time.sleep(5)
    results = driver.find_element(By.TAG_NAME, "pre").text
    print("RESULTS:", results)
    assert "MSFT" in results
    assert "AAPL" in results
    print("Valid tickers display test passed.")
    driver.quit()

def test_invalid_ticker_reported():
    driver = get_driver()
    ticker_input = driver.find_element(By.NAME, "tickers")
    analyze_btn = driver.find_element(By.ID, "analyze-btn")
    ticker_input.clear()
    ticker_input.send_keys("INVALID")
    analyze_btn.click()
    time.sleep(5)
    results = driver.find_element(By.TAG_NAME, "pre").text
    print("RESULTS:", results)
    assert "INVALID" in results or "ignored" in results
    print("Invalid ticker reporting test passed.")
    driver.quit()

if __name__ == "__main__":
    print("Running Selenium tests...")  
    test_valid_tickers_display_ytd()
    test_invalid_ticker_reported()
    test_spinner_and_button_disabled()