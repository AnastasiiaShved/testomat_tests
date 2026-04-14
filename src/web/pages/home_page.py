from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page, base_url: str, app_base_url: str) -> None:
        self.page = page
        self.__base_url = base_url
        self.__app_base_url = app_base_url

    def open(self):
        self.page.goto(self.__base_url)

    def is_loaded(self):
        expect(self.page.locator("#headerMenuWrapper")).to_be_visible()
        expect(self.page.locator(".side-menu .login-item")).to_have_text('Log in')
        expect(self.page.locator(".side-menu .start-item")).to_have_text('Start for free')

    def click_login(self):
        self.page.get_by_text("Log in", exact=True).click()
        self.page.wait_for_url(f"{self.__app_base_url}/**", timeout=15000)
