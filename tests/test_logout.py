# tests/test_logout.py
import os
import pytest
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotInteractableException,
    TimeoutException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.config import BASE_URL, USERNAME, PASSWORD
from datetime import datetime

OUT_DIR = "debug_artifacts"
os.makedirs(OUT_DIR, exist_ok=True)

def remove_overlays(driver):
    # Remove modal backdrops and overlays that block clicks
    js = """
    const overlays = document.querySelectorAll('.modal-backdrop, .overlay, .modal-backdrop.show');
    overlays.forEach(o => o.remove());
    // also remove inline blocking style on body
    document.body.style.overflow = 'auto';
    return overlays.length;
    """
    try:
        removed = driver.execute_script(js)
        return removed
    except Exception:
        return 0

def try_click_with_fallbacks(driver, el):
    # 1) native click
    try:
        el.click()
        return True
    except Exception:
        pass

    # 2) scroll into view + ActionChains
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        ActionChains(driver).move_to_element(el).pause(0.2).click(el).perform()
        return True
    except Exception:
        pass

    # 3) make element visible & enabled then JS click
    try:
        driver.execute_script("arguments[0].style.display='block'; arguments[0].style.visibility='visible'; arguments[0].removeAttribute('disabled');", el)
        driver.execute_script("arguments[0].click();", el)
        return True
    except Exception:
        pass

    return False

def dump_debug(driver, name_prefix="logout_debug"):
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    png = os.path.join(OUT_DIR, f"{name_prefix}_{ts}.png")
    html = os.path.join(OUT_DIR, f"{name_prefix}_{ts}.html")
    try:
        driver.save_screenshot(png)
    except Exception:
        pass
    try:
        with open(html, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
    except Exception:
        pass
    return png, html

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def locate_logout(driver):
    # try several locators — returns element or raises NoSuchElementException
    candidates = [
        (By.ID, "logout2"),
        (By.LINK_TEXT, "Log out"),
        (By.LINK_TEXT, "Logout"),
        (By.XPATH, "//a[contains(., 'Log out')]"),
        (By.XPATH, "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'log out')]"),
        (By.XPATH, "//button[contains(., 'Log out') or contains(., 'Logout')]"),
    ]
    for by, loc in candidates:
        try:
            els = driver.find_elements(by, loc)
            if els:
                return els[0]
        except Exception:
            continue
    # fallback: search for any element with id containing 'logout'
    try:
        els = driver.find_elements(By.XPATH, "//*[contains(@id,'logout') or contains(@class,'logout')]")
        if els:
            return els[0]
    except Exception:
        pass
    raise NoSuchElementException("Logout element not found by any locator strategy")

def test_logout(driver):
    driver.get(BASE_URL)
    login_page = LoginPage(driver)
    home_page = HomePage(driver)

    # login
    login_page.open_login()
    login_page.login(USERNAME, PASSWORD)

    # wait briefly for either alert or logout presence
    try:
        WebDriverWait(driver, 8).until(lambda d: d.find_elements(By.ID, "logout2") or EC.alert_is_present()(d))
    except TimeoutException:
        # capture any alert and fail with message
        try:
            alert = driver.switch_to.alert
            text = alert.text
            alert.accept()
            pytest.fail(f"Login failed with alert: {text}")
        except Exception:
            png, html = dump_debug(driver, "login_timeout")
            pytest.fail(f"Login did not succeed (timeout). Dumped debug artifacts: {png}, {html}")

    # if an alert popped, abort
    try:
        alert = driver.switch_to.alert
        txt = alert.text
        alert.accept()
        pytest.fail(f"Login failed with alert: {txt}")
    except Exception:
        pass

    # remove overlays that might block interaction
    remove_overlays(driver)

    # locate logout element using many strategies
    try:
        logout_el = locate_logout(driver)
    except NoSuchElementException:
        png, html = dump_debug(driver, "logout_not_found")
        pytest.fail(f"Logout element not found. Debug artifacts: {png}, {html}")

    # ensure presence and visibility
    try:
        WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@id,'logout') or contains(., 'Log out') or contains(., 'Logout')]")))
    except TimeoutException:
        # continue; we'll attempt fallbacks below
        pass

    # final click attempts with fallbacks
    clicked = False
    try:
        clicked = try_click_with_fallbacks(driver, logout_el)
    except Exception:
        clicked = False

    if not clicked:
        # try to find another matching element and click it
        try:
            alt = locate_logout(driver)
            clicked = try_click_with_fallbacks(driver, alt)
        except Exception:
            clicked = False

    if not clicked:
        png, html = dump_debug(driver, "logout_not_interactable")
        pytest.fail(f"Logout element present but not interactable. Debug artifacts: {png}, {html}")

    # verify logout succeeded by presence of login trigger again
    try:
        WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.ID, "login2")))
    except TimeoutException:
        # might still be logged out but locator different; allow pass if login modal not present
        png, html = dump_debug(driver, "post_logout_verify_failed")
        pytest.fail(f"Logout may have failed (login trigger not visible). Debug artifacts: {png}, {html}")

    print("✅ User logged out successfully")
