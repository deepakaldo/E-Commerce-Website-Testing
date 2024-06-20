import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.test_excel_utils import read_excel

@pytest.fixture(scope="module") #this excute the yield after all test_data is tested and in end it excute yield
def browser():
    serv_obj = Service("C:/chromedriver-win64/chromedriver.exe")  # Ensure this path is correct
    driver = webdriver.Chrome(service=serv_obj)
    yield driver
    driver.quit()

# Use read_excel to get the test data
test_data = read_excel("C:/Users/Deepak/PycharmProjects/testing/data/logintestdata.xlsx", "Sheet1")

@pytest.mark.parametrize("username, password", test_data) #when you use @pytest.mark.parametrize("username, password", test_data),
# pytest will generate and execute separate test cases for each tuple in test_data. For each test case, it will pass the corresponding username and password values to the test function
def test_login(browser, username, password):
    browser.get("https://demo.nopcommerce.com/login?returnUrl=%2F")
    browser.find_element(By.ID, "Email").clear()
    browser.find_element(By.ID, "Email").send_keys(username)
    browser.find_element(By.ID, "Password").clear()
    browser.find_element(By.ID, "Password").send_keys(password)
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    assert "Log out" in browser.page_source  # Check for the presence of the "Log out" link in the page source
