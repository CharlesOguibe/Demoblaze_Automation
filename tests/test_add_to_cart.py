import pytest
from selenium import webdriver
from pages.home_page import HomePage
from utils.config import BASE_URL

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_add_to_cart(driver):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    home_page.add_item_to_cart("Nokia lumia 1520")
    print("✅ Product successfully added to cart")
