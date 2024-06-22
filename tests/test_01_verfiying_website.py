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
def test_title(browser):
    expected_title="nopCommerce demo store"
    page_title=browser.title
    page_title_url=browser.current_url
    print(page_title_url)
    print(page_title)
    assert page_title == expected_title, "Test failed: Expected title '{}' but got '{}'".format(expected_title,page_title)