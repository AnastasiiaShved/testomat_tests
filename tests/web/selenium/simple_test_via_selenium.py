from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.web.selenium.components.profile_menu import ProfileMenu
from src.web.selenium.pages import LoginPage
from src.web.selenium.pages.login_pageV2 import LoginPageV2
from tests.fixtures.config import Config


def test_selenium_login_and_search(driver: WebDriver, config: Config):
    wait = WebDriverWait(driver, 10, poll_frequency=0.5,
                         ignored_exceptions=[NoSuchElementException, StaleElementReferenceException])

    driver.get(config.app_base_url)
    driver.find_element(By.CSS_SELECTOR, value="#content-desktop #user_email").send_keys(config.email)
    driver.find_element(By.CSS_SELECTOR, value="#content-desktop #user_password").send_keys(config.password)
    driver.find_element(By.CSS_SELECTOR, value="#content-desktop [value='Sign In']").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#content-desktop .common-flash-success")))

    target_project = "Brown PLC"
    driver.find_element(By.CSS_SELECTOR, value="#content-desktop #search").send_keys(target_project)
    driver.find_element(By.CSS_SELECTOR, value=f"#content-desktop [title='{target_project}']").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f".breadcrumbs-page [title='{target_project}']")))


def test_login_with_page_object(driver: WebDriver, config: Config):
    login_page = LoginPage(driver)
    login_page.open(config.app_base_url)
    login_page.is_loaded()
    login_page.login_user(config.email, config.password)
    login_page.should_see_message()


def test_login_and_logout(driver: WebDriver, config: Config):
    login_page = LoginPage(driver)
    login_page.open(config.app_base_url)
    login_page.is_loaded()
    login_page.login_user(config.email, config.password)
    login_page.should_see_message()

    profile_menu = ProfileMenu(driver)
    profile_menu.sign_out()

    login_page.is_loaded()


def test_sign_out(logged_driver: WebDriver):
    profile_menu = ProfileMenu(logged_driver)
    profile_menu.sign_out()

    login_page = LoginPage(logged_driver)
    login_page.is_loaded()


def test_login_with_page_object_v2(driver: WebDriver, config: Config):
    login_page = LoginPageV2(driver)
    login_page.open(config.app_base_url)
    login_page.is_loaded()
    login_page.login_user(config.email, config.password)
    login_page.should_see_success_message()
