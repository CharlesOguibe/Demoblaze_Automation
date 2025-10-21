import pytest
import time
from selenium import webdriver
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.cart_page import CartPage
from utils.config import BASE_URL, USERNAME, PASSWORD

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_checkout(driver):
    driver.get(BASE_URL)

    # Step 1: Add item to cart
    home_page = HomePage(driver)
    home_page.add_item_to_cart("Nokia lumia 1520")

    # Step 2: Open Cart
    cart_page = CartPage(driver)
    cart_page.open_cart()

    # Step 3: Place Order
    checkout_page = CheckoutPage(driver)
    checkout_page.place_order("Charles", "Nigeria", "Lagos", "1234567890123456", "12", "2025")
    time.sleep(2)

    print("✅ Checkout flow completed successfully")
