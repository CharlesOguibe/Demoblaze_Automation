class SignupPage:
    def __init__(self, driver):
        self.driver = driver

    def open_signup(self):
        self.driver.find_element("id", "signin2").click()

    def signup(self, username, password):
        self.driver.find_element("id", "sign-username").send_keys(username)
        self.driver.find_element("id", "sign-password").send_keys(password)
        self.driver.find_element("xpath", "//button[text()='Sign up']").click()
