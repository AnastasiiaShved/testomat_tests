import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.web.selenium.core.base_page import BasePage


class LoginPageV2(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @property
    @allure.step
    def form(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop form#new_user")

    @property
    @allure.step
    def email(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_email")

    @property
    @allure.step
    def password(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_password")

    @property
    @allure.step
    def remember_me_checkbox(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_remember_me")

    @property
    @allure.step
    def sign_in_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop [value='Sign In']")

    @property
    @allure.step
    def success_message(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop .common-flash-success")

    @property
    @allure.step
    def error_message(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop .common-flash-error")

    @property
    @allure.step
    def forgot_password_link(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop a[href*='password']")

    @allure.step
    def open(self, url: str) -> None:
        self.driver.get(url)

    @allure.step
    def is_loaded(self) -> None:
        self.driver.find_element(By.CSS_SELECTOR, "#content-desktop form#new_user")

    @allure.step
    def login_user(self, email: str, password: str, remember_me_checkbox: bool = False) -> None:
        self.email.clear()
        self.email.send_keys(email)
        self.password.clear()
        self.password.send_keys(password)
        if remember_me_checkbox and not self.remember_me_checkbox.is_selected():
            self.remember_me_checkbox.click()
        self.sign_in_button.click()

    @allure.step
    def should_see_success_message(self) -> None:
        self.driver.find_element(By.CSS_SELECTOR, "#content-desktop .common-flash-success")

    @allure.step
    def should_see_error_message(self) -> None:
        self.driver.wait.for_visible(By.CSS_SELECTOR, "#content-desktop .common-flash-error")
