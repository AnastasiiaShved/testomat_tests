from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.web.selenium.core.base_page import BasePage


class LoginPageV2(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @property
    def form(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop form#new_user")

    @property
    def email(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_email")

    @property
    def password(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_password")

    @property
    def remember_me_checkbox(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_remember_me")

    @property
    def sign_in_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop [value='Sign In']")

    @property
    def success_message(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop .common-flash-success")

    @property
    def error_message(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop .common-flash-error")

    @property
    def forgot_password_link(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop a[href*='password']")

    def open(self, url: str) -> None:
        self.driver.get(url)

    def is_loaded(self) -> None:
        self.driver.find_element(By.CSS_SELECTOR, "#content-desktop form#new_user")

    def login_user(self, email: str, password: str, remember_me_checkbox: bool = False) -> None:
        self.email.clear()
        self.email.send_keys(email)
        self.password.clear()
        self.password.send_keys(password)
        if remember_me_checkbox and not self.remember_me_checkbox.is_selected():
            self.remember_me_checkbox.click()
        self.sign_in_button.click()

    def should_see_success_message(self) -> None:
        self.driver.find_element(By.CSS_SELECTOR, "#content-desktop .common-flash-success")

    def should_see_error_message(self) -> None:
        self.driver.wait.for_visible(By.CSS_SELECTOR, "#content-desktop .common-flash-error")
