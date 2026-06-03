import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from src.web.selenium.core.base_page import BasePage


class ProfileMenu(BasePage):
    AVATAR_BUTTON = (By.CSS_SELECTOR, "#user-menu-button")
    DROPDOWN_MENU = (By.CSS_SELECTOR, "#profile-menu")
    SIGNED_IN_EMAIL = (By.CSS_SELECTOR, ".auth-header-nav-right-dropdown-menu-block-email")
    MY_COMPANIES_LINK = (By.CSS_SELECTOR, "a[href='/companies']")
    ACCOUNT_LINK = (By.CSS_SELECTOR, ".auth-header-nav-right-dropdown-menu-block-account a[href='/account']")
    DOWNLOADS_LINK = (By.CSS_SELECTOR, "a[href='/account/files']")
    FREE_TRIAL_LINK = (By.CSS_SELECTOR, "a[href='/trials']")
    SIGN_OUT_BUTTON = (By.CSS_SELECTOR, "form[action='/users/sign_out'] button")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @allure.step
    def open_menu(self) -> None:
        self.click(self.AVATAR_BUTTON)
        self.wait.for_visible(self.DROPDOWN_MENU)

    @allure.step
    def get_signed_in_email(self) -> str:
        return self.get_text(self.SIGNED_IN_EMAIL)

    @allure.step
    def sign_out(self) -> None:
        self.open_menu()
        self.click(self.SIGN_OUT_BUTTON)

    @allure.step
    def go_to_account(self) -> None:
        self.open_menu()
        self.click(self.ACCOUNT_LINK)

    @allure.step
    def go_to_my_companies(self) -> None:
        self.open_menu()
        self.click(self.MY_COMPANIES_LINK)

    @allure.step
    def go_to_downloads(self) -> None:
        self.open_menu()
        self.click(self.DOWNLOADS_LINK)

    @allure.step
    def go_to_free_trial(self) -> None:
        self.open_menu()
        self.click(self.FREE_TRIAL_LINK)
