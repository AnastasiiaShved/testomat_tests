import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from src.web.selenium.core.base_page import BasePage


class LoginPage(BasePage):
    FORM = (By.CSS_SELECTOR, "#content-desktop form#new_user")
    EMAIL = (By.CSS_SELECTOR, "#content-desktop #user_email")
    PASSWORD = (By.CSS_SELECTOR, "#content-desktop #user_password")
    SIGN_IN_BUTTON = (By.CSS_SELECTOR, "#content-desktop [value='Sign In']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "#content-desktop .common-flash-success")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @allure.step
    def open(self, url: str) -> None:
        self.driver.get(url)

    @allure.step
    def is_loaded(self) -> None:
        self.wait.for_visible(self.FORM)

    @allure.step
    def login_user(self, email: str, password: str) -> None:
        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)
        self.click(self.SIGN_IN_BUTTON)

    @allure.step
    def should_see_message(self) -> None:
        self.wait.for_visible(self.SUCCESS_MESSAGE)
