import pytest
import time
from selenium import webdriver
from pages.cart_page import CartPage
from pages.home_page import HomePage
from utils.config import BASE_URL, USERNAME, PASSWORD

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_remove_from_cart(driver):
    driver.get(BASE_URL)

    # Add an item to cart first
    home_page = HomePage(driver)
    home_page.add_item_to_cart("Nokia lumia 1520")

    # Open the cart
    cart_page = CartPage(driver)
    cart_page.open_cart()

    # Remove the item
    cart_page.remove_item("Nokia lumia 1520")
    time.sleep(2)

    print("✅ Item successfully removed from cart")
