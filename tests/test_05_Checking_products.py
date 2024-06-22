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

@allure.severity(allure.severity_level.NORMAL)
def test_prices_displayed(browser):
    search_input = browser.find_element(By.ID, "small-searchterms")
    search_input.send_keys("Asus N551JK-XO076H Laptop")
    search_input.send_keys(Keys.RETURN)
    product_link = browser.find_element(By.XPATH,"//a[contains(text(),'Asus N551JK-XO076H Laptop')]")
    product_link.click()
    # Verify price is correctly displayed
    price_element = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='price actual-price']"))
    )
    price_text = price_element.text
    # Assuming the expected price is "$999.00", you can modify it accordingly
    expected_price = "$1,350.00"
    assert price_text == expected_price

@allure.severity(allure.severity_level.MINOR)
def test_related_product_recommendations(browser):
    search_input = browser.find_element(By.ID, "small-searchterms")
    search_input.send_keys("Asus N551JK-XO076H Laptop")
    search_input.send_keys(Keys.RETURN)
    product_link = browser.find_element(By.XPATH,"//a[contains(text(),'Asus N551JK-XO076H Laptop')]")
    product_link.click()
    # Check for related product recommendations
    related_products = WebDriverWait(browser, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='item-grid']")))
    assert len(related_products) > 0  # Ensure at least one related product is displayed

@allure.severity(allure.severity_level.CRITICAL)
def test_product_images_displayed_correctly(browser):
    search_input = browser.find_element(By.ID, "small-searchterms")
    search_input.send_keys("Asus N551JK-XO076H Laptop")
    search_input.send_keys(Keys.RETURN)
    product_link = browser.find_element(By.XPATH, "//a[contains(text(),'Asus N551JK-XO076H Laptop')]")
    product_link.click()
    # Verify product images are displayed correctly
    product_images = WebDriverWait(browser, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='picture']//img"))
    )
    for image in product_images:
        assert image.is_displayed()