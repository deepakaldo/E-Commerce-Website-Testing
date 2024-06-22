import pytest
from selenium import webdriver
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

@allure.severity(allure.severity_level.CRITICAL)
def test_registration(browser):
    browser.find_element(By.XPATH,"//a[normalize-space()='Register']").click()
    browser.find_element(By.ID, "gender-male").click()
    browser.find_element(By.ID, "FirstName").send_keys("sathiya")
    browser.find_element(By.ID, "LastName").send_keys("murthi")
    date=Select(browser.find_element(By.XPATH,"//select[@name='DateOfBirthDay']"))
    date.select_by_value("27")
    month=Select(browser.find_element(By.XPATH,"//select[@name='DateOfBirthMonth']"))
    month.select_by_visible_text("may")
    year=Select(browser.find_element(By.XPATH,"//select[@name='DateOfBirthYear']"))
    year.select_by_value("2000")
    browser.find_element(By.ID, "Email").send_keys("sathiyamurthi9989@example.com")
    browser.find_element(By.ID, "Password").send_keys("Test@123456")
    browser.find_element(By.ID, "ConfirmPassword").send_keys("Test@123456")

    # Submit the registration form
    browser.find_element(By.ID, "register-button").click()

    # Wait for the registration confirmation message
    wait = WebDriverWait(browser, 10)
    confirmation_message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "result")))

    # Verify registration was successful
    assert "Your registration completed" in confirmation_message.text

@allure.severity(allure.severity_level.CRITICAL)
def test_valid_email(browser):
    browser.find_element(By.XPATH,"//a[normalize-space()='Register']").click()
    browser.find_element(By.ID, "Email").send_keys("johndoe")
    browser.find_element(By.XPATH,"//button[@id='register-button']").click()
    browser.find_element(By.ID, "register-button").click()
    error = browser.find_element(By.XPATH, "//span[@id='Email-error']")
    assert "Please enter a valid email address" in error.text

@allure.severity(allure.severity_level.CRITICAL)
def test_password(browser):
    browser.find_element(By.XPATH,"//a[normalize-space()='Register']").click()
    browser.find_element(By.ID, "gender-male").click()
    browser.find_element(By.ID, "FirstName").send_keys("John")
    browser.find_element(By.ID, "LastName").send_keys("Doe")
    browser.find_element(By.ID, "Email").send_keys("johndoe@example.com")
    browser.find_element(By.ID, "Password").send_keys("a")
    browser.find_element(By.ID, "ConfirmPassword").send_keys("a")
    # Submit the registration form
    browser.find_element(By.ID, "register-button").click()
    error_mesg=browser.find_element(By.XPATH,"//span[@class='field-validation-error']")
    assert "<p>Password must meet the following rules: </p><ul><li>must have at least 6 characters and not greater than 64 characters</li></ul>" in error_mesg.text

# def main():
#     pytest.main(["-v", "--alluredir=allure-results"])
#
# if __name__ == "__main__":
#     main()