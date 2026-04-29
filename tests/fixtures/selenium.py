import pytest
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from src.web.selenium.pages.login_page import LoginPage
from tests.fixtures.config import Config


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(0)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def logged_driver(driver: WebDriver, config: Config) -> WebDriver:
    login_page = LoginPage(driver)
    login_page.open(config.app_base_url)
    login_page.is_loaded()
    login_page.login_user(config.email, config.password)
    login_page.should_see_message()
    yield driver
