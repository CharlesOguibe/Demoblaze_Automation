# pages/checkout_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def _safe_send(self, by, locator, value):
        try:
            el = self.wait.until(EC.presence_of_element_located((by, locator)))
            el.clear()
            el.send_keys(value)
        except Exception:
            # element might not exist in some builds; ignore quietly
            pass

    def place_order(self, name, country, city, card, month, year):
        """
        Fill the checkout modal fields and press Purchase.
        Returns: confirmation text (alert or DOM) or None.
        """
        # Fill known fields (ids used on demoblaze-like pages)
        self._safe_send(By.ID, "name", name)
        self._safe_send(By.ID, "country", country)
        self._safe_send(By.ID, "city", city)
        self._safe_send(By.ID, "card", card)
        self._safe_send(By.ID, "month", month)
        self._safe_send(By.ID, "year", year)

        # Click Purchase button (try multiple strategies)
        purchase_btn_locators = [
            (By.XPATH, "//button[text()='Purchase']"),
            (By.CSS_SELECTOR, "button[onclick='purchaseOrder()']"),
            (By.CSS_SELECTOR, "#orderModal .modal-footer button")
        ]

        clicked = False
        for by, locator in purchase_btn_locators:
            try:
                btn = self.wait.until(EC.element_to_be_clickable((by, locator)))
                btn.click()
                clicked = True
                break
            except Exception:
                continue

        if not clicked:
            # As a last resort try executing click via JS on the first matching element
            try:
                el = self.driver.find_element(By.XPATH, "//button[text()='Purchase']")
                self.driver.execute_script("arguments[0].click();", el)
                clicked = True
            except Exception:
                pass

        # After clicking, wait for either an alert OR a confirmation element in DOM
        conf_text = None
        try:
            # Wait until either alert is present OR DOM confirmation exists
            def either_alert_or_dom(drv):
                # alert
                if EC.alert_is_present()(drv):
                    return True
                # common DOM confirmation patterns
                dom_selectors = [
                    "//h2[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'thank')]",
                    "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'thank you')]",
                    "//*[contains(@id, 'order') and contains(., 'Thank')]",
                    "//*[contains(@class, 'sweet-alert')]",
                    "//*[@id='orderModal' and contains(., 'Thank')]"
                ]
                for s in dom_selectors:
                    try:
                        if drv.find_elements(By.XPATH, s):
                            return True
                    except Exception:
                        continue
                return False

            WebDriverWait(self.driver, 10).until(either_alert_or_dom)
        except Exception:
            # nothing appeared within timeout
            return None

        # If alert present, capture and return its text
        try:
            alert = self.driver.switch_to.alert
            conf_text = alert.text
            alert.accept()
            return conf_text
        except Exception:
            pass

        # Otherwise grab the first matching DOM confirmation text
        dom_xpaths = [
            "//h2[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'thank')]",
            "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'thank you for your purchase')]",
            "//*[@id='orderModal']",
            "//*[contains(@class, 'sweet-alert')]"
        ]
        for xp in dom_xpaths:
            try:
                els = self.driver.find_elements(By.XPATH, xp)
                if els:
                    text = els[0].text.strip()
                    if text:
                        return text
            except Exception:
                continue

        # As fallback, return non-empty body text near top (rare)
        try:
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            preview = body_text[:200].strip()
            return preview if preview else None
        except Exception:
            return None
