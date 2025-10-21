import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    def __init__(self, driver):
        self.driver = driver

    def open_cart(self):
        """Navigates to the cart page."""
        cart_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))
        )
        cart_link.click()
        time.sleep(2)

    def remove_item(self, product_name):
        """Removes a specific item from the cart."""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//td[text()='{product_name}']/following-sibling::td/a"))
        )
        remove_btn = self.driver.find_element(By.XPATH, f"//td[text()='{product_name}']/following-sibling::td/a")
        remove_btn.click()
        time.sleep(2)
