import pytest
import time
from selenium import webdriver
from pages.signup_page import SignupPage
from utils.config import BASE_URL
from utils.helpers import generate_random_user

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_signup(driver):
    driver.get(BASE_URL)
    signup_page = SignupPage(driver)
    username, password = generate_random_user()
    signup_page.open_signup()
    time.sleep(1)
    signup_page.signup(username, password)
    time.sleep(3)
    print("✅ Signup test completed successfully")
