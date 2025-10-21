import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

    def place_order(self, name, country, city, card, month, year):
        """Completes the checkout form and confirms the purchase."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Place Order']"))
        ).click()

        # Fill the order form
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "name"))
        )
        self.driver.find_element(By.ID, "name").send_keys(name)
        self.driver.find_element(By.ID, "country").send_keys(country)
        self.driver.find_element(By.ID, "city").send_keys(city)
        self.driver.find_element(By.ID, "card").send_keys(card)
        self.driver.find_element(By.ID, "month").send_keys(month)
        self.driver.find_element(By.ID, "year").send_keys(year)

        self.driver.find_element(By.XPATH, "//button[text()='Purchase']").click()
        time.sleep(2)

        # Confirm success popup
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Thank you for your purchase!']"))
        )
        self.driver.find_element(By.XPATH, "//button[text()='OK']").click()
        time.sleep(2)
