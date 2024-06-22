
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

@pytest.fixture(scope="function")
def browser():
    serv_obj = Service("C:\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=serv_obj)
    driver.get("https://demo.nopcommerce.com/")
    driver.maximize_window()
    yield driver
    driver.quit()

@allure.severity(allure.severity_level.CRITICAL)
def test_search_displays_products(browser):
    search_input = browser.find_element(By.ID, "small-searchterms")
    search_input.send_keys("laptop")
    search_input.send_keys(Keys.RETURN)

    # Wait for the search results to load
    search_results = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-item"))
    )

    # Assert that search results are displayed
    assert len(search_results) > 0

@allure.severity(allure.severity_level.MINOR)
def test_empty_search_field(browser):
    search_input = browser.find_element(By.ID, "small-searchterms")
    search_input.send_keys("")
    search_input.send_keys(Keys.RETURN)

    # Wait for the no results message
    no_results_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='warning']")))

    # Assert that the proper message for empty search field is displayed
    assert "Search term minimum length is 3 characters" in no_results_message.text

@allure.severity(allure.severity_level.MINOR)
def test_search_with_misspelled_keywords(browser):
    browser.get("https://demo.nopcommerce.com/")
    search_input = browser.find_element(By.ID, "small-searchterms")
    search_input.send_keys("lapptop")
    search_input.send_keys(Keys.RETURN)


    # Wait for the no results message or suggestions to appear
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results")))

    # Check for no results message or product suggestions
    no_results_message = browser.find_element(By.CSS_SELECTOR, ".no-result")
    assert "No products were found that matched your criteria." in no_results_message.text

