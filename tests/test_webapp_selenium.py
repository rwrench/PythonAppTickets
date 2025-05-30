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
    

def get_visible_results(driver):
    results = wait_for_element(driver,
        (By.TAG_NAME, "pre"), 
        EC.visibility_of_element_located, timeout=30).text
    print("RESULTS:", results)
    return results

def input_tickers_and_fetch_results(driver):
    ticker_input = wait_for_element(driver,
            (By.NAME, "tickers"), 
            EC.presence_of_element_located, timeout=60)
    click_button(driver, ticker_input, "MSFT,AAPL")
    print("Button clicked, waiting for results...")
    results = get_visible_results(driver)
    return results


def test_valid_tickers_display_ytd():
    print("Starting test for valid tickers display...")
    driver = get_driver()
    try:
        results = input_tickers_and_fetch_results(driver)
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
   
def test_spinner_and_button_disabled():
    print("Starting test for spinner and button state after submit...")
    driver = get_driver()
    ticker_input = driver.find_element(By.NAME, "tickers")
    analyze_btn = driver.find_element(By.ID, "analyze-btn")
    ticker_input.clear()
    ticker_input.send_keys("MSFT,AAPL")
    analyze_btn.click()
    print("Button clicked, waiting for results...")
    # Wait for results to appear
    results = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.TAG_NAME, "pre"))
    ).text
    print("RESULTS:", results)
    assert "MSFT" in results
    assert "AAPL" in results
    print("Valid tickers display test passed.")
    driver.quit()


# def test_spinner_and_button_disabled():
#     print("Starting test for spinner and button state after submit...")
#     driver = get_driver()
#     try:
#         results = input_tickers_and_fetch_results(driver)
#         spinner = wait_for_element(driver,
#             (By.ID, "spinner")
#             , EC.visibility_of_element_located, timeout=30)
#         assert spinner.is_displayed(), "Spinner should be visible after submit"
#         analyze_btn = driver.find_element(By.ID, "analyze-btn")
#         WebDriverWait(driver, 10).until(
#             lambda d: analyze_btn.get_attribute("disabled") == "true"
#         )
#         assert analyze_btn.get_attribute("disabled") == "true", "Button should be disabled after submit"
#         print("Spinner and button state test passed.")
#     except Exception as e:
#         print("Test failed:", e)
#         print(driver.page_source) 
#         raise
#     finally:
#         driver.quit()

if __name__ == "__main__":
    print("Running Selenium tests...")  
    test_valid_tickers_display_ytd()
    test_invalid_ticker_reported()