import pytest
import time
from selenium import webdriver
from pages.login_page import LoginPage
from utils.config import BASE_URL, USERNAME, PASSWORD

@pytest.fixture
def driver():
    # Auto-manage driver (works from Selenium 4.6+)
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_valid_login(driver):
    driver.get(BASE_URL)
    login_page = LoginPage(driver)
    login_page.open_login()
    time.sleep(2)
    login_page.login(USERNAME, PASSWORD)
    time.sleep(3)
    print("✅ Login test completed successfully")
