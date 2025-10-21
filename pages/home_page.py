import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def add_item_to_cart(self, product_name):
        """Selects a product and adds it to the cart."""
        wait = WebDriverWait(self.driver, 15)

        # Click the product
        product = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, product_name)))
        product.click()

        # Wait for product page to load
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Add to cart']")))

        # Click 'Add to cart'
        add_button = self.driver.find_element(By.XPATH, "//a[text()='Add to cart']")
        add_button.click()

        # Wait for the alert and accept it
        wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()

        # Go back to home page
        self.driver.find_element(By.ID, "nava").click()

        time.sleep(1)

    def logout(self):
        """Logs out the current user."""
        wait = WebDriverWait(self.driver, 15)
        logout_button = wait.until(EC.element_to_be_clickable((By.ID, "logout2")))
        logout_button.click()