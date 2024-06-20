import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
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
def test_product_quantity(browser):
    search_input = browser.find_element(By.ID, "small-searchterms")
    search_input.send_keys("Asus N551JK-XO076H Laptop")
    search_input.send_keys(Keys.RETURN)
    product_link = browser.find_element(By.XPATH, "//a[contains(text(),'Asus N551JK-XO076H Laptop')]")
    product_link.click()
    browser.find_element(By.XPATH,"//button[@id='add-to-cart-button-5']").click()
    browser.find_element(By.XPATH,"//li[@id='topcartlink']").click()
    act=ActionChains(browser)
    quantiy=browser.find_element(By.XPATH,"//div[contains(@class, 'quantity up')]")
    act.double_click(quantiy).perform()
    updated_quantity_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'qty-input')]"))
    )
    updated_quantity = int(updated_quantity_input.get_attribute("value"))
    assert updated_quantity == 3

@allure.severity(allure.severity_level.MINOR)
def test_gift(browser):
    browser.get("https://demo.nopcommerce.com/cart")
    search_input = browser.find_element(By.ID, "small-searchterms")
    search_input.send_keys("Asus N551JK-XO076H Laptop")
    search_input.send_keys(Keys.RETURN)
    product_link = browser.find_element(By.XPATH, "//a[contains(text(),'Asus N551JK-XO076H Laptop')]")
    product_link.click()
    browser.find_element(By.XPATH, "//button[@id='add-to-cart-button-5']").click()
    browser.find_element(By.XPATH, "//li[@id='topcartlink']").click()
    gift_wrapping_dropdown = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "checkout_attribute_1")))

    select=Select(gift_wrapping_dropdown)
    select.select_by_visible_text("Yes [+$10.00]")
    selected_option = select.first_selected_option
    assert selected_option.text == "Yes [+$10.00]"

@allure.severity(allure.severity_level.CRITICAL)
def test_apply_discount_code(browser):
    browser.get("https://demo.nopcommerce.com/cart")
    search_input = browser.find_element(By.ID, "small-searchterms")
    search_input.send_keys("Asus N551JK-XO076H Laptop")
    search_input.send_keys(Keys.RETURN)
    product_link = browser.find_element(By.XPATH, "//a[contains(text(),'Asus N551JK-XO076H Laptop')]")
    product_link.click()
    browser.find_element(By.XPATH, "//button[@id='add-to-cart-button-5']").click()
    browser.find_element(By.XPATH, "//li[@id='topcartlink']").click()
    # Wait for the discount code input to be present
    discount_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "discountcouponcode"))
    )

    # Apply a discount code
    discount_input.send_keys("123")
    apply_discount_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.NAME, "applydiscountcouponcode"))
    )
    apply_discount_button.click()

    # Verify the discount is applied
    discount_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='message-success']"))
    )
    assert "The coupon code was applied" in discount_message.text