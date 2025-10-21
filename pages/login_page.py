# Install selenium in your environment if missing: pip install selenium
try:
    from selenium.webdriver.common.by import By
except Exception:
    # Fallback for editors/linters when selenium isn't installed
    class By:
        ID = "id"
        XPATH = "xpath"

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.login_link = (By.ID, "login2")
        self.username_input = (By.ID, "loginusername")
        self.password_input = (By.ID, "loginpassword")
        self.login_button = (By.XPATH, "//button[text()='Log in']")

    def open_login(self):
        self.driver.find_element(*self.login_link).click()

    def login(self, username, password):
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()
