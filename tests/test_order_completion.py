import pytest
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import allure


@pytest.fixture(scope="function")
def browser():
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False,
        'profile.default_content_setting_values.automatic_downloads': 1
    }
    chrome_options.add_experimental_option('prefs', prefs)

    # Add the below arguments to start Chrome in incognito mode and to ensure the browser is controlled by automation
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    serv_obj = Service("C:/chromedriver-win64/chromedriver.exe")  # Use forward slashes for the path
    driver = webdriver.Chrome(service=serv_obj, options=chrome_options)
    driver.get("https://demo.nopcommerce.com/")
    driver.maximize_window()
    yield driver
    driver.quit()

@allure.severity(allure.severity_level.CRITICAL)
def test_checkout_completed(browser):  # Use 'browser' fixture name here
    driver = browser
    search_input = browser.find_element(By.ID, "small-searchterms")
    search_input.clear()
    search_input.send_keys("Asus N551JK-XO076H Laptop")
    search_input.send_keys(Keys.RETURN)
    product_link = browser.find_element(By.XPATH, "//a[contains(text(),'Asus N551JK-XO076H Laptop')]")
    product_link.click()
    browser.find_element(By.XPATH, "//button[@id='add-to-cart-button-5']").click()
    browser.find_element(By.XPATH, "//li[@id='topcartlink']").click()
    act = ActionChains(browser)
    quantiy = browser.find_element(By.XPATH, "//div[contains(@class, 'quantity up')]")
    act.double_click(quantiy).perform()

    #selecting_gift_wrapping
    gift_wrapping_dropdown = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "checkout_attribute_1")))
    select = Select(gift_wrapping_dropdown)
    select.select_by_visible_text("Yes [+$10.00]")

    #Appling_couponcoe
    discount_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "discountcouponcode"))
    )
    discount_input.send_keys("123")

    # Agree to terms of service and proceed to checkout
    driver.find_element(By.ID, "termsofservice").click()
    driver.find_element(By.ID, "checkout").click()
    driver.find_element(By.XPATH,"//button[normalize-space()='Checkout as Guest']").click()

    # Fill in the checkout details (assuming the user is not logged in and needs to enter billing details)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "BillingNewAddress_FirstName"))
    )
    driver.find_element(By.ID, "BillingNewAddress_FirstName").send_keys("John")
    driver.find_element(By.ID, "BillingNewAddress_LastName").send_keys("Doe")
    driver.find_element(By.ID, "BillingNewAddress_Email").send_keys("johndoe@example.com")
    country=Select(driver.find_element(By.XPATH, "//select[@id='BillingNewAddress_CountryId']"))
    country.select_by_visible_text("India")
    driver.find_element(By.XPATH,"//input[@id='BillingNewAddress_City']").send_keys("coimbatore")
    driver.find_element(By.XPATH,"//input[@id='BillingNewAddress_Address1']").send_keys("44/4 Nanjappan Street")
    driver.find_element(By.ID, "BillingNewAddress_ZipPostalCode").send_keys("10001")
    driver.find_element(By.ID, "BillingNewAddress_PhoneNumber").send_keys("1234567890")
    driver.find_element(By.XPATH, "//button[@onclick='if (!window.__cfRLUnblockHandlers) return false; Billing.save()']").click()

    #shipping_method
    shipping_method = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='button-1 shipping-method-next-step-button']"))
    )
    shipping_method.click()

    #payment_method
    payment_button= WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,"//button[@class='button-1 payment-method-next-step-button']"))
    )
    payment_button.click()


    #payment_information
    payment_info=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='button-1 payment-info-next-step-button']")))
    payment_info.click()
    driver.save_screenshot("before_checkout_completed.png")

    # Confirm the order
    confirm_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Confirm']"))
    )

    # Ensure the confirm button is visible and enabled
    WebDriverWait(driver, 10).until(EC.visibility_of(confirm_button))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(confirm_button))

    confirm_button.click()

    driver.save_screenshot("after_checkout_completed.png")


    # Verify the order completion
    confirmation_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//strong[normalize-space()='Your order has been successfully processed!']"))
    )

    assert "Your order has been successfully processed!" in confirmation_message.text