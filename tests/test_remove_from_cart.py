import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.cart_page import CartPage
from pages.home_page import HomePage
from utils.config import BASE_URL

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

    # Wait until the cart item row is present (use class or specific locator your page object relies on)
    # Example expects a cart table row contains the product name; adjust selector if needed.
    WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH, "//td[text()='Nokia lumia 1520']")))

    # Click the delete/remove button for that item — the page object method should perform the click,
    # but we guard with an explicit wait inside the test to avoid TimeoutException.
    # If your CartPage.remove_item does the waiting internally you can call it directly.
    delete_locator = (By.XPATH, "//a[text()='Delete']")
    WebDriverWait(driver, 7).until(EC.element_to_be_clickable(delete_locator)).click()

    # Wait for the item row to disappear from the cart
    WebDriverWait(driver, 7).until(EC.invisibility_of_element_located((By.XPATH, "//td[text()='Nokia lumia 1520']")))

    print("✅ Item successfully removed from cart")
