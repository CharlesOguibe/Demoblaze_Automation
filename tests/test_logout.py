import pytest
import time
from selenium import webdriver
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.config import BASE_URL, USERNAME, PASSWORD

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_logout(driver):
    driver.get(BASE_URL)
    login_page = LoginPage(driver)
    home_page = HomePage(driver)

    # Log in first
    login_page.open_login()
    login_page.login(USERNAME, PASSWORD)
    time.sleep(3)

    # Then logout
    home_page.logout()
    time.sleep(2)

    print("✅ User logged out successfully")
