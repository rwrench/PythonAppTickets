from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os


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

def wait_for_ticker_input(driver, timeout=20):
    """Wait for the ticker input element to be present and return it."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.NAME, "tickers"))
    )

# def test_spinner_and_button_disabled():
    driver = get_driver()
    ticker_input = driver.find_element(By.NAME, "tickers")
    analyze_btn = driver.find_element(By.ID, "analyze-btn")
    ticker_input.clear()
    ticker_input.send_keys("MSFT,AAPL,INVALID")
    analyze_btn.click()
    # Wait for spinner to appear
    spinner = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "spinner"))
    )
    assert spinner.is_displayed(), "Spinner should be visible after submit"
    # Wait for button to be disabled
    WebDriverWait(driver, 10).until(
        lambda d: analyze_btn.get_attribute("disabled") == "true"
    )
    assert analyze_btn.get_attribute("disabled") == "true", "Button should be disabled after submit"
    print("Spinner and button state test passed.")
    driver.quit()

def test_valid_tickers_display_ytd():
    print("Starting test for valid tickers display...")
    driver = get_driver()
    try:
        ticker_input = wait_for_ticker_input(driver, timeout=60)  # Wait up to 60 seconds
        analyze_btn = driver.find_element(By.ID, "analyze-btn")
        ticker_input.clear()
        ticker_input.send_keys("MSFT,AAPL")
        analyze_btn.click()
        print("Button clicked, waiting for results...")
        results = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.TAG_NAME, "pre"))
        ).text
        print("RESULTS:", results)
        assert "MSFT" in results
        assert "AAPL" in results
        print("Valid tickers display test passed.")
    except Exception as e:
        print("Test failed:", e)
        print(driver.page_source)  # Add this line
        raise
    finally:
        driver.quit()

# # def test_invalid_ticker_reported():
#     driver = get_driver()
#     # Wait for the ticker input to be present
#     ticker_input = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.NAME, "tickers"))
#     )
#     analyze_btn = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "analyze-btn"))
#     )
#     ticker_input.clear()
#     ticker_input.send_keys("INVALID")
#     analyze_btn.click()
#     # Wait for results to appear
#     results = WebDriverWait(driver, 15).until(
#         EC.visibility_of_element_located((By.TAG_NAME, "pre"))
#     ).text
#     print("RESULTS:", results)
#     assert "INVALID" in results or "ignored" in results
#     print("Invalid ticker reporting test passed.")
#     driver.quit()

if __name__ == "__main__":
    print("Running Selenium tests...")  
    test_valid_tickers_display_ytd()
    # test_invalid_ticker_reported()
    # test_spinner_and_button_disabled()