from selenium.webdriver.common.by import By
import time

class ProductPage:
    def __init__(self, driver):
        self.driver = driver
        self.product_link = (By.LINK_TEXT, "Samsung galaxy s6")
        self.add_to_cart_button = (By.LINK_TEXT, "Add to cart")

    def open_product(self):
        self.driver.find_element(*self.product_link).click()
        time.sleep(2)

    def add_to_cart(self):
        self.driver.find_element(*self.add_to_cart_button).click()
        time.sleep(2)
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        return alert_text
